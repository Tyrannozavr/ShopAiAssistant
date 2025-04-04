from typing import Annotated

from fastapi import Depends

from depends.db import db_dep
from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision
from services.interaction_service import InteractionService
from core.Config import settings

def get_chatgpt_vision_service():
    return ChatGPTVision()

def get_chatgpt_service():
    return ChatGPT()  # Placeholder for actual implementation

def get_gpt_interaction_service(db: db_dep):
    return InteractionService(db=db, api_key=settings.openai_key, base_url=settings.openai_url)

interaction_service_dep = Annotated[InteractionService, Depends(get_gpt_interaction_service)]