from typing import List

from fastapi import APIRouter, Depends, Body
from fastapi import UploadFile
from sqlalchemy.orm import Session

from core.logging_config import logger
from depends.chatgpt import get_chatgpt_vision_service, get_chatgpt_service
from depends.db import get_db
from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision

router = APIRouter()


@router.post("/photo")
async def process_photo(
        photo: UploadFile,
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: str = Body(...),
        db: Session = Depends(get_db),
        chatgpt_service: ChatGPTVision = Depends(get_chatgpt_vision_service)
):
    logger.info(f"Processing photo for user {user_id}")
    result = chatgpt_service.process_photo(user_id=user_id, photo_file=photo.file, door_type=door_type,
                                           priorities=priorities, user_request=user_request, db=db)
    return {"result": result}

@router.post("/question")
async def process_photo(
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: str = Body(...),
        db: Session = Depends(get_db),
        chatgpt_service: ChatGPT = Depends(get_chatgpt_service)
):
    logger.info(f"Processing photo for user {user_id}")
    result = chatgpt_service.get_response(user_id=user_id, door_type=door_type, priorities=priorities,
                                          question=user_request, db=db)
    return {"result": result}

