from ast import literal_eval
from typing import List

from fastapi import APIRouter, Depends, Body, UploadFile

from core.logging_config import logger
from depends.chatgpt import get_chatgpt_vision_service, get_chatgpt_service, interaction_service_dep
from depends.db import db_dep
from models import Configuration
from services.chatgpt import ChatGPT
from services.chatgptvision import ChatGPTVision
from services.limit_checker import check_limit, get_random_joke

router = APIRouter()


@router.post("/photo")
async def process_photo(
        db: db_dep,
        photo: UploadFile,
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: str = Body(...),
        chatgpt_service: ChatGPTVision = Depends(get_chatgpt_vision_service)
):
    photo_limit = db.query(Configuration).filter(Configuration.key == "photo_limit").first()
    if photo_limit is None:
        photo_limit = Configuration(key="photo_limit", value="3")
        db.add(photo_limit)
        db.commit()
        db.refresh(photo_limit)
    photo_limit = int(photo_limit.value)

    # Check if the user has reached the photo limit
    if check_limit(user_id=user_id, db=db, limit_key="photo", limit_value=photo_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "result": joke}

    logger.debug(f"Processing photo for user {user_id}")
    img_size = db.query(Configuration).filter(Configuration.key == "image_size").first()
    if img_size is None:
        img_size = Configuration(key="image_size", value="(600, 600)")
        db.add(img_size)
        db.commit()
        db.refresh(img_size)
    img_size = literal_eval(img_size.value)
    img_height, img_width = img_size
    result = chatgpt_service.process_photo(user_id=user_id, photo_file=photo.file, door_type=door_type,
                                           priorities=priorities, user_request=user_request, db=db,
                                           img_width=img_width, img_height=img_height)
    return {"result": result}


@router.post("/question")
async def process_question(
        db: db_dep,
        door_type: str = Body(...),
        priorities: List[str] = Body(...),
        user_request: str = Body(...),
        user_id: str = Body(...),
        chatgpt_service: ChatGPT = Depends(get_chatgpt_service)
):
    question_limit = db.query(Configuration).filter(Configuration.key == "question_limit").first()
    if question_limit is None:
        question_limit = Configuration(key="question_limit", value="5")
        db.add(question_limit)
        db.commit()
        db.refresh(question_limit)
    question_limit = int(question_limit.value)
    if check_limit(user_id=user_id, db=db, limit_key="question", limit_value=question_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "result": joke}

    logger.debug(f"Processing question for user {user_id}")
    # return "Helllworld"
    result = chatgpt_service.get_response(user_id=user_id, door_type=door_type, priorities=priorities,
                                          question=user_request, db=db)
    return {"result": result}


@router.post("/chat")
async def process_question(
        db: db_dep,
        interaction_service: interaction_service_dep,
        user_request: str = Body(...),
        user_id: str = Body(...),
):
    question_limit = db.query(Configuration).filter(Configuration.key == "question_limit").first()
    if question_limit is None:
        question_limit = Configuration(key="question_limit", value="5")
        db.add(question_limit)
        db.commit()
        db.refresh(question_limit)
    question_limit = int(question_limit.value)
    if check_limit(user_id=user_id, db=db, limit_key="question", limit_value=question_limit):
        joke = get_random_joke(db)
        return {"message": "Daily limit reached", "result": joke}

    logger.debug(f"Processing question for user {user_id}")
    result = interaction_service.start_interaction(user_id=user_id, user_message=user_request)
    return {"result": result}
