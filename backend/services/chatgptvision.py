import os
import base64
import uuid
from openai import OpenAI
from sqlalchemy.orm import Session

from core.Config import MEDIA_ROOT, MEDIA_URL
from core.logging_config import logger
from models import Configuration, ChatGPTInteraction
from PIL import Image
from io import BytesIO

class ChatGPTVision:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("PROXYAPI_API_KEY"),  # Ensure you have this key in your environment variables
            base_url="https://api.proxyapi.ru/openai/v1"
        )
        self.image_storage_path = MEDIA_ROOT  # Define where to store images

    def get_prompt_template(self, db: Session, key: str) -> str:
        config = db.query(Configuration).filter(Configuration.key == key).first()
        if not config:
            raise ValueError("Prompt template not found in the database.")
        return str(config.value)

    def update_prompt(self, template: str, door_type: str, priorities: list, user_request: str) -> str:
        return template.format(door_type=door_type, priorities=", ".join(priorities), user_request=user_request)

    def process_photo(self, photo_file, door_type: str, priorities: list, user_request: str, db: Session):
        prompt = self.create_prompt(db, door_type, priorities, user_request)
        base64_image = self.prepare_image(photo_file)
        response_content = self.send_request(prompt, base64_image)
        photo_url = self.save_image(photo_file)
        self.store_interaction(db, prompt, response_content, photo_url)
        return response_content

    def create_prompt(self, db: Session, door_type: str, priorities: list, user_request: str) -> str:
        prompt_template = self.get_prompt_template(db, "photo_prompt")
        prompt = self.update_prompt(prompt_template, door_type, priorities, user_request)
        logger.info(f"Generated prompt: {prompt}")
        return prompt

    def prepare_image(self, photo_file) -> str:
        image = Image.open(photo_file).convert("RGB")
        image = image.resize((600, 600))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def send_request(self, prompt: str, base64_image: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        return response.choices[0].message.content

    def save_image(self, photo_file) -> str:
        image = Image.open(photo_file).convert("RGB")
        unique_filename = f"{uuid.uuid4()}.jpg"  # Generate a unique filename using uuid4
        image_path = os.path.join(self.image_storage_path, unique_filename)
        image.save(image_path, format="JPEG")
        return f"{MEDIA_URL}{unique_filename}"  # Construct the URL using MEDIA_URL

    def store_interaction(self, db: Session, prompt: str, response: str, photo_url: str):
        interaction = ChatGPTInteraction(prompt=prompt, response=response, photo_url=photo_url)
        db.add(interaction)
        db.commit()