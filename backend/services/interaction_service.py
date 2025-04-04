import json
from sqlalchemy.orm import Session
from models import ChatGPTInteraction
from openai import OpenAI
from typing import Dict, Optional


class InteractionService:
    def __init__(self, db: Session, api_key: str, base_url: str):
        self.db = db
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.default_prompt = ("Ты консультант по дверям. Разговаривай по-человечески: понятно, с заботой. В ходе диалога "
                               "постарайся помочь пользователю определиться с выбором двери, узнать его контактные данные"
                               "чтобы он мог продолжить общение с менеджером")
        self.system_prompt = (
                self.default_prompt + "Отвечай строго в JSON формате: "
                                      "{'response': твой ответ пользователю, 'contact_data': null или контактные данные если пользователь их предоставил, "
                                      "'summary': null или краткое описание потребностей пользователя (заполняется ТОЛЬКО когда пользователь предоставил контактные данные, "
                                      "содержит ключевую информацию: тип двери, требования, бюджет, сроки и другие важные детали из диалога)}. "
                                      "Формат summary должен быть кратким и информативным для менеджера. "
                                      "Не добавляй никакого текста вокруг JSON. "
                                      "Если контактные данные не предоставлены, summary должен быть null."
        )
        self.history_depth = 3

    def _get_chat_history(self, telegram_id: str) -> list:
        """Получает историю диалога для пользователя"""
        return self.db.query(ChatGPTInteraction).filter(
            ChatGPTInteraction.user_id == telegram_id
        ).order_by(ChatGPTInteraction.datetime.desc()).limit(self.history_depth).all()

    def _prepare_messages(self, telegram_id: str, user_message: str) -> list:
        """Подготавливает список сообщений для OpenAI API"""
        history = self._get_chat_history(telegram_id)
        messages = [{"role": "system", "content": self.system_prompt}]

        for interaction in history:
            messages.append({"role": "user", "content": interaction.prompt})
            try:
                response_data = json.loads(interaction.response)
                messages.append({"role": "assistant", "content": response_data.get('response', '')})
            except json.JSONDecodeError:
                messages.append({"role": "assistant", "content": interaction.response})

        messages.append({"role": "user", "content": user_message})
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

    def start_interaction(self, telegram_id: str, user_message: str) -> Dict:
        """Основной метод для обработки взаимодействия с пользователем"""
        try:
            messages = self._prepare_messages(telegram_id, user_message)
            print("Prompt is ", messages)
            response = self.client.chat.completions.create(
                messages=messages,
                model="o3-mini",  # Используйте актуальную модель
                # max_tokens=20000,  # Более реалистичное значение
                response_format={"type": "json_object"}  # Гарантирует JSON ответ
            )

            # Получаем и возвращаем результат
            response_content = response.choices[0].message.content
            response_data = self._parse_response(response_content)

            # Сохраняем взаимодействие
            interaction = ChatGPTInteraction(
                user_id=telegram_id,
                prompt=user_message,
                response=json.dumps(response_data, ensure_ascii=False)
            )
            self.db.add(interaction)
            self.db.commit()

            # Если есть контактные данные, очищаем историю
            if response_data.get('contact_data'):
                self.db.query(ChatGPTInteraction).filter(
                    ChatGPTInteraction.user_id == telegram_id
                ).delete()
                self.db.commit()

            return response_data

        except Exception as e:
            print(f"Error in chat completion: {e}")
            return {
                'response': "Извините, произошла ошибка. Попробуйте позже.",
                'contact_data': None,
                'summary': None
            }