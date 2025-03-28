from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Configuration
from depends.db import get_db

app = FastAPI()

@app.get("/config/{key}")
async def get_config(key: str, db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return {"key": config.key, "value": config.value}

@app.post("/config/{key}")
async def set_config(key: str, value: str, db: Session = Depends(get_db)):
    config = db.query(Configuration).filter(Configuration.key == key).first()
    if config:
        config.value = value
    else:
        config = Configuration(key=key, value=value)
        db.add(config)
    db.commit()
    return {"message": "Configuration updated successfully"}
