import os
import base64
from openai import OpenAI
from sqlalchemy.orm import Session

from core.logging_config import logger
from models import Configuration
from PIL import Image
from io import BytesIO

class ChatGPT:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("PROXYAPI_API_KEY"),  # Ensure you have this key in your environment variables
            base_url="https://api.proxyapi.ru/openai/v1"
        )

    def get_prompt_template(self, db: Session, key: str) -> str:
        config = db.query(Configuration).filter(Configuration.key == key).first()
        if not config:
            raise ValueError("Prompt template not found in the database.")
        return str(config.value)

    def update_prompt(self, template: str, door_type: str, priorities: list, user_request: str) -> str:
        return template.format(door_type=door_type, priorities=", ".join(priorities), user_request=user_request)

    def process_photo(self, photo_file, door_type: str, priorities: list, user_request: str, db: Session):
        # Get the prompt template from the database
        prompt_template = self.get_prompt_template(db, "photo_prompt")

        # Update the prompt with actual data
        prompt = self.update_prompt(prompt_template, door_type, priorities, user_request)
        logger.info(f"Generated prompt: {prompt}")

        # Validate and resize the photo if necessary
        image = Image.open(photo_file)
        # if image.size != (1024, 1024):
        #     image = image.resize((1024, 1024))
        image = image.resize((700, 700))
        # Convert the image to base64
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)
        base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Send the request to the proxy API using the OpenAI client
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},  # Your question
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"  # For Base64
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,  # Adjust as needed
        )

        return response.choices[0].message.content