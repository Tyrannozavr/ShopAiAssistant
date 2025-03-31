import base64
import os
import uuid
from io import BytesIO

from PIL import Image
from sqlalchemy.orm import Session

from core.Config import MEDIA_ROOT, MEDIA_URL
from models import ChatGPTInteraction
from services.chatgpt import ChatGPT


class ChatGPTVision(ChatGPT):
    def __init__(self):
        super().__init__()
        self.prompt_key = "photo_prompt"  # Set a different key for retrieving the prompt
        self.image_storage_path = MEDIA_ROOT  # Define where to store images

    def process_photo(self, db: Session, user_id: str, photo_file, door_type: str, priorities: list, user_request: str = "",
                      img_height: int = 600, img_width: int = 600) -> str:
        prompt = self.get_prompt_template(db)
        prompt = self.update_prompt(template=prompt, question=user_request, priorities=priorities, door_type=door_type)
        base64_image = self.prepare_image(photo_file, img_height=img_height, img_width=img_width)
        response_content = self._send_request(prompt, base64_image)
        photo_url = self.save_image(photo_file)
        self.store_interaction(prompt=prompt, response=response_content, photo_url=photo_url, db=db, user_id=user_id)
        return response_content

    def _send_request(self, prompt: str, base64_image: str) -> str:
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

    def store_interaction(self, user_id: str, db: Session, prompt: str, response: str, photo_url: str):
        interaction = ChatGPTInteraction(user_id=user_id, prompt=prompt, response=response, photo_url=photo_url)
        db.add(interaction)
        db.commit()

    def prepare_image(self, photo_file, img_height: int = 600, img_width: int = 600) -> str:
        image = Image.open(photo_file).convert("RGB")
        image = image.resize((img_width, img_height))
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def save_image(self, photo_file) -> str:
        image = Image.open(photo_file).convert("RGB")
        unique_filename = f"{uuid.uuid4()}.jpg"  # Generate a unique filename using uuid4
        image_path = os.path.join(self.image_storage_path, unique_filename)
        image.save(image_path, format="JPEG")
        return f"{MEDIA_URL}{unique_filename}"  # Construct the URL using MEDIA_URL