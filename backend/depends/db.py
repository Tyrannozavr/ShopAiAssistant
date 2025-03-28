from typing import Annotated

from fastapi import Depends

from db import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dep = Annotated[SessionLocal, Depends(get_db)]