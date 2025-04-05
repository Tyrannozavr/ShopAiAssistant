import json
from sqlalchemy.orm import Session

from core.logging_config import logger
from models import ChatGPTInteraction
from openai import OpenAI
from typing import Dict, Optional

from repositories.orders import get_current_user_order


class InteractionService:
    def __init__(self, db: Session, api_key: str, base_url: str):
        self.db = db
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.default_prompt = ("Выступи в роли специалиста по продаже дверей."
                               " Разговаривай по-человечески: понятно, с заботой. В ходе диалога "
                               "постарайся помочь пользователю определиться с выбором двери, узнать его контактные данные "
                               "чтобы он мог продолжить общение с менеджером. Указывай контактные данные только если пользователь "
                               "оставил их в последнем сообщении.")
        self.system_prompt = (
                self.default_prompt + "Отвечай строго в JSON формате: "
                                      "{'response': твой ответ пользователю, 'contact_data': null или контактные данные, "
                                      "'summary': структурированная сводка всех ключевых требований из диалога}. "

                                      "Формат summary: кратко, только факты для менеджера: "
                                      "- Основной запрос (дверь входная/межкомнатная, материал)"
                                      "- Конкретные параметры (размеры, особенности)"
                                      "- Бюджет и сроки если указаны"
                                      "- Особые пожелания "

                                      "Обновляй summary при каждом сообщении, сохраняя все важные детали. "
                                      "Не добавляй текст вокруг JSON."
        )
        self.history_depth = 3

    def _get_chat_history(self, user_id: str) -> list:
        """Получает историю диалога для пользователя"""
        return self.db.query(ChatGPTInteraction).filter(
            ChatGPTInteraction.user_id == user_id
        ).order_by(ChatGPTInteraction.datetime.desc()).limit(self.history_depth).all()

    def _prepare_messages(self, user_id: str, user_message: str, file_type: str = None,
                          file_description: str = None) -> list:
        history = self._get_chat_history(user_id)
        last_summary = {}

        # Ищем последний summary в истории
        for interaction in reversed(history):
            try:
                last_response = json.loads(interaction.response)
                if "summary" in last_response:
                    last_summary = last_response["summary"]
                    break
            except json.JSONDecodeError:
                continue

        # Добавляем summary в системное сообщение
        system_message = {
            "role": "system",
            "content": f"{self.system_prompt}\n\nТекущий контекст (НЕ МЕНЯЙ его без запроса пользователя): {last_summary}"
        }

        messages = [system_message]

        # Добавляем последние 3 сообщения (user+assistant)
        for interaction in history[-3:]:
            messages.append({"role": "user", "content": interaction.prompt})
            try:
                assistant_response = json.loads(interaction.response).get("response", "")
            except json.JSONDecodeError:
                assistant_response = interaction.response
            messages.append({"role": "assistant", "content": assistant_response})

        # Текущее сообщение пользователя
        current_message = user_message
        if file_type and file_description:
            current_message += f"\n[Прикреплён файл: {file_description}]"

        messages.append({"role": "user", "content": current_message})
        return messages

    def _parse_response(self, response_content: str) -> Dict:
        """Парсит ответ от OpenAI, обрабатывая возможные ошибки"""
        try:
            return json.loads(response_content)
        except json.JSONDecodeError:
            # Попытка извлечь JSON из текста, если он обернут в другие символы
            try:
                start = response_content.find('{')
                end = response_content.rfind('}') + 1
                return json.loads(response_content[start:end])
            except:
                return {
                    'response': response_content,
                    'contact_data': None,
                    'summary': None
                }

    def start_interaction(self, user_id: str, user_message: str, file_type: str = None,
                          file_description: str = None) -> Dict:
        """Основной метод для обработки взаимодействия с пользователем"""
        try:
            messages = self._prepare_messages(user_id, user_message, file_type=file_type,
                                              file_description=file_description)
            logger.info(f"Messages for user {user_id}: {messages}")
            # print("Prompt is ", messages)
            response = self.client.chat.completions.create(
                messages=messages,
                model="o3-mini",  # Используйте актуальную модель
                response_format={"type": "json_object"}  # Гарантирует JSON ответ
            )

            # Получаем и возвращаем результат
            if not response or not response.choices or len(response.choices) == 0:
                logger.error(f"Invalid API response for user {user_id}: {response}")
                return {
                    "response": "Извините, произошла ошибка при обработке запроса",
                    "contact_data": None,
                    "summary": None
                }
            response_content = response.choices[0].message.content
            response_data = self._parse_response(response_content)

            # Сохраняем взаимодействие
            interaction = ChatGPTInteraction(
                user_id=user_id,
                prompt=user_message,
                response=json.dumps(response_data, ensure_ascii=False)
            )
            self.db.add(interaction)
            self.db.commit()

            # Если есть контактные данные, очищаем историю
            if response_data.get('contact_data'):
                order = get_current_user_order(self.db, user_id=user_id)
                if order:
                    order.contact_data = response_data.get("contact_data")
                    order.gpt_summary = response_data.get('summary')
                    order.is_completed = True
                    self.db.add(order)
                    self.db.commit()
                history = self.db.query(ChatGPTInteraction).filter(
                    ChatGPTInteraction.user_id == user_id and ChatGPTInteraction.is_finished == False
                )
                for interaction in history:
                    interaction.is_finished = True
                    self.db.add(interaction)
                self.db.commit()

            return response_data

        except Exception as e:
            print(f"Error in chat completion: {e}")
            return {
                'response': "Извините, произошла ошибка. Попробуйте позже.",
                'contact_data': None,
                'summary': None
            }