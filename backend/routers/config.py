from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from models import Configuration
from depends.db import get_db, db_dep

router = APIRouter()

@router.get("/config/{key}")
async def get_config(db: db_dep, key: str):
    config = db.query(Configuration).filter(Configuration.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"key": config.key, "value": config.value}

@router.post("/config/{key}")
async def set_config(db: db_dep, key: str, value: str):
    config = db.query(Configuration).filter(Configuration.key == key).first()
    if config:
        config.value = value
    else:
        config = Configuration(key=key, value=value)
        db.add(config)
    db.commit()
    return {"message": "Configuration updated successfully"}
