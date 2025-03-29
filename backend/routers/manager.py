from fastapi import APIRouter, Body
from starlette.requests import Request

from core.logging_config import logger
from depends.db import db_dep
from repositories.manager import get_manager_by_identifier

router = APIRouter()

@router.post("/register_chat")
async def register_chat(db: db_dep, identifier: str = Body(), chat_id: str = Body()):
    manager = get_manager_by_identifier(db, identifier)
    manager.chat_id = chat_id
    db.commit()
    return {"message": "Вы успешно зарегистрировали чат"}