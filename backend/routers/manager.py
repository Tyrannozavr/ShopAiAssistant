from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from depends.db import db_dep
from repositories.manager import get_manager_by_identifier

router = APIRouter()

@router.post("/register_chat")
async def register_chat(identifier: str, chat_id: str, db: db_dep):
    manager = get_manager_by_identifier(db, identifier)
    manager.chat_id = chat_id
    db.commit()
    return {"message": "Chat ID registered successfully"}