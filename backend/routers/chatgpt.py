from typing import List
from fastapi import APIRouter, Depends, Body, UploadFile
from sqlalchemy.orm import Session
from core.logging_config import logger
from depends.chatgpt import get_chatgpt_vision_service, get_chatgpt_service
from depends.db import get_db
from models import Configuration
from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision
from services.limit_checker import check_limit, get_random_joke

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
    photo_limit = db.query(Configuration).filter(Configuration.key == "photo_limit").first()
    photo_limit = int(photo_limit.value)

    # Check if the user has reached the photo limit
    if check_limit(user_id=user_id, db=db, limit_key="photo", limit_value=photo_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "joke": joke}

    logger.info(f"Processing photo for user {user_id}")
    result = chatgpt_service.process_photo(user_id=user_id, photo_file=photo.file, door_type=door_type,
                                           priorities=priorities, user_request=user_request, db=db)
    return {"result": result}
    if check_limit(user_id=user_id, db=db, limit_key="photo", limit_value=photo_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "joke": joke}

    logger.info(f"Processing photo for user {user_id}")
    result = chatgpt_service.process_photo(user_id=user_id, photo_file=photo.file, door_type=door_type,
                                           priorities=priorities, user_request=user_request, db=db)
    return {"result": result}

@router.post("/question")
async def process_question(
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: str = Body(...),
        db: Session = Depends(get_db),
        chatgpt_service: ChatGPT = Depends(get_chatgpt_service)
):
    question_limit = db.query(Configuration).filter(Configuration.key == "question_limit").first()
    question_limit = int(question_limit.value)
    if check_limit(user_id=user_id, db=db, limit_key="question", limit_value=question_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "joke": joke}

    logger.info(f"Processing question for user {user_id}")
    result = chatgpt_service.get_response(user_id=user_id, door_type=door_type, priorities=priorities,
                                          question=user_request, db=db)
    return {"result": result}
