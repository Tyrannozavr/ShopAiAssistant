from typing import Optional

from fastapi import Body
from sqlalchemy import exists
from sqlalchemy.orm import Session

from models import Order


def get_current_user_order(db: Session, user_id: str) -> Optional[Order]:
    return (db.query(Order)
            .filter(Order.user_id == user_id)
            .filter(Order.is_completed == False)
            .order_by(Order.id.desc()).first()
            )

def check_current_user_order_exists(db: Session, user_id: str) -> bool:
    return db.query(exists().where(
        Order.user_id == user_id,
        Order.is_completed == False
    )).scalar()
