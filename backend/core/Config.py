import os
from pathlib import Path

from pydantic_settings import BaseSettings
BASE_DIR = Path(__file__).resolve().parent.parent


# Define the base URL for media files
MEDIA_URL = os.getenv("MEDIA_URL", "/static/media/")

# Define the directory where media files will be stored
MEDIA_ROOT = os.path.join(os.getcwd(), "static", "media")

# Ensure the media directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)

class Settings(BaseSettings):
    openai_key: str
    openai_url: str
    admin_username: str = "admin"
    admin_password: str = "123456"
    database_url: str = "sqlite:///db.sqlite3"
    bot_token: str


    class Config:
        env_file = BASE_DIR / ".env"

print(BASE_DIR)
settings = Settings()