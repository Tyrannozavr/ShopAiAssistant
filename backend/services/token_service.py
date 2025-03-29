import jwt
from datetime import datetime, timedelta
from models import Manager

# Secret key for encoding and decoding JWT tokens
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Token expiration time

def create_access_token(manager: Manager, expires_delta: timedelta = None):
    to_encode = {
        "user_id": manager.id,
        "identifier": manager.identifier,
        "username": manager.username,
        "city": manager.city.name if manager.city else None,
        "is_staff": manager.is_staff,
        "is_admin": manager.is_admin,
        "chat_id": manager.chat_id
    }
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return the entire payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token has expired")
    except jwt.PyJWTError:
        raise ValueError("Invalid token")