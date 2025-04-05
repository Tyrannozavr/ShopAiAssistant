from typing import Annotated, Literal, Optional

from fastapi import Depends, Body

from core.Config import settings
from depends.db import db_dep
from models import Order
from repositories.orders import get_current_user_order
from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision
from services.interaction_service import InteractionService
from services.telegram.files import TelegramAudioTranscriber, TelegramImageDescriber, FileTranscriber


def get_chatgpt_vision_service():
    return ChatGPTVision()


def get_chatgpt_service():
    return ChatGPT()  # Placeholder for actual implementation


def get_gpt_interaction_service(db: db_dep):
    return InteractionService(db=db, api_key=settings.openai_key, base_url=settings.openai_url)


FileType = Literal["voice", "document", "photo"]


def get_file_type(file_type: Optional[FileType] = Body(None)) -> Literal["voice", "document", "photo"] | None:
    return file_type


file_type_dep = Annotated[Optional[FileType], Depends(get_file_type)]


def get_file_transcriber(file_type: file_type_dep) -> FileTranscriber | None:
    if file_type == "voice":
        return TelegramAudioTranscriber(api_key=settings.openai_key, base_url=settings.openai_url,
                                        bot_token=settings.bot_token)
    elif file_type == "document" or file_type == "photo":
        return TelegramImageDescriber(api_key=settings.openai_key, base_url=settings.openai_url,
                                      bot_token=settings.bot_token)
    elif file_type is None:
        return None
    else:
        raise ValueError("Unsupported file type")


interaction_service_dep = Annotated[InteractionService, Depends(get_gpt_interaction_service)]
files_transcriber_dep = Annotated[FileTranscriber, Depends(get_file_transcriber)]


current_order_dep = Annotated[Optional[Order], Depends(get_current_user_order)]