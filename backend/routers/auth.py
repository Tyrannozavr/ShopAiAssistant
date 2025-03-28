from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session

from services.auth_service import verify_password
from services.token_service import create_access_token
from repositories.manager import get_manager_by_username
from depends.db import get_db

router = APIRouter()

@router.post("/login")
async def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    manager = get_manager_by_username(db, username)
    if not manager or not verify_password(password, manager.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token(manager)
    return {"access_token": access_token, "token_type": "bearer"}