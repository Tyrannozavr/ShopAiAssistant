from sqlalchemy import func
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from models import ChatGPTInteraction, Jokes
from core.logging_config import logger
import random

def check_limit(user_id: str, db: Session, limit_key: str, limit_value: int) -> bool:
    # Get the current date in UTC
    now = datetime.now(timezone.utc)
    start_of_day = datetime.combine(now.date(), datetime.min.time(), tzinfo=timezone.utc)
    end_of_day = datetime.combine(now.date(), datetime.max.time(), tzinfo=timezone.utc)

    # Base query for counting interactions
    query = db.query(ChatGPTInteraction).filter(
        ChatGPTInteraction.user_id == user_id,
        ChatGPTInteraction.datetime >= start_of_day,
        ChatGPTInteraction.datetime <= end_of_day
    )
    logger.info(f"22Count is {query.count()}")
    # Adjust the query based on the limit_key
    if limit_key == "photo":
        query = query.filter(ChatGPTInteraction.photo_url.isnot(None))
    elif limit_key == "question":
        query = query.filter(ChatGPTInteraction.photo_url.is_(None))
    logger.info(f"11Count is {query.count()}")

    # Count interactions for the user today
    interaction_count = query.count()
    logger.info(f"User {user_id} has {interaction_count} interactions today for {limit_key}")

    # Check if the user has reached the limit
    return interaction_count >= limit_value

def get_random_joke(db: Session) -> str:
    # Get a random joke from the Jokes model
    joke = db.query(Jokes).order_by(func.random()).first()
    return joke.text if joke else "No jokes available at the moment."