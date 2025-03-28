from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.logging_config import logger
from depends.chatgpt import get_chatgpt_service
from depends.db import get_db
from services.chatgpt import ChatGPT

router = APIRouter()


@router.post("/photo")
async def process_photo(
        photo: UploadFile,
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: int = Body(...),
        db: Session = Depends(get_db),
        chatgpt_service: ChatGPT = Depends(get_chatgpt_service)
):
    logger.info(f"Processing photo for user {user_id}")
    result = chatgpt_service.process_photo(photo.file, door_type, priorities, user_request, db)
    return {"result": result}
