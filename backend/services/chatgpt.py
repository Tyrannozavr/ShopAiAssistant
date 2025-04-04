import os
from openai import OpenAI
from sqlalchemy.orm import Session

from core.logging_config import logger
from models import Configuration, ChatGPTInteraction

class ChatGPT:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("PROXYAPI_API_KEY"),  # Ensure you have this key in your environment variables
            base_url="https://api.proxyapi.ru/openai/v1"
        )
        self.prompt_key = "question_prompt"  # Set a different key for retrieving the prompt

    def get_prompt_template(self, db: Session) -> str:
        config = db.query(Configuration).filter(Configuration.key == self.prompt_key).first()
        if config is None:
            config = Configuration(key=self.prompt_key, value="Question: {question}\nPriorities: {priorities}\nDoor type: {door_type}")
            db.add(config)
            db.commit()
            db.refresh(config)
        return str(config.value)

    def update_prompt(self, template: str, question: str, priorities: list, door_type: str) -> str:
        return template.format(question=question, priorities=", ".join(priorities), door_type=door_type)

    def get_response(self, user_id: str, question: str, priorities: list, door_type: str, db: Session) -> str:
        prompt_template = self.get_prompt_template(db)
        prompt = self.update_prompt(question=question, priorities=priorities, door_type=door_type, template=prompt_template)
        response_content = self._send_request(prompt)
        self.store_interaction(db=db, user_id=user_id, prompt=prompt, response=response_content)
        return response_content

    def _send_request(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

    def store_interaction(self, db: Session, user_id: str, prompt: str, response: str):
        interaction = ChatGPTInteraction(user_id=user_id, prompt=prompt, response=response)
        db.add(interaction)
        db.commit()
