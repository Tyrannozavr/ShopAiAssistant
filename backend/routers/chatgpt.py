from typing import List

from fastapi import APIRouter, Depends
from fastapi import UploadFile
from sqlalchemy.orm import Session

from depends.chatgpt import get_chatgpt_service
from depends.db import get_db
from services.chatgpt import ChatGPT

router = APIRouter()


@router.post("/photo")
async def process_photo(
        photo: UploadFile,
        door_type: str,
        priorities: List[str],
        user_request: str,
        db: Session = Depends(get_db),
        chatgpt_service: ChatGPT = Depends(get_chatgpt_service)
):
    result = chatgpt_service.process_photo(photo.file, door_type, priorities, user_request, db)
    return {"result": result}
