from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from models import ChatGPTInteraction, Jokes
from core.logging_config import logger
import random

def check_limit(user_id: str, db: Session, limit_key: str, limit_value: int) -> bool:
    # Get the current date
    today = datetime.now().date()

    # Count interactions for the user today
    interaction_count = db.query(ChatGPTInteraction).filter(
        ChatGPTInteraction.user_id == user_id,
        ChatGPTInteraction.datetime >= datetime.combine(today, datetime.min.time()),
        ChatGPTInteraction.datetime <= datetime.combine(today, datetime.max.time())
    ).count()

    logger.info(f"User {user_id} has {interaction_count} interactions today for {limit_key}")

    # Check if the user has reached the limit
    if interaction_count >= limit_value:
        return True
    return False

def get_random_joke(db: Session) -> str:
    # Get a random joke from the Jokes model
    joke = db.query(Jokes).order_by(func.random()).first()
    return joke.message if joke else "No jokes available at the moment."