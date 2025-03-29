from fastapi import Depends, HTTPException, Cookie
from fastapi.security import OAuth2PasswordBearer

from models import Manager
from services.token_service import decode_access_token
from schemas.manager import TokenData
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def decode_token(token: str) -> TokenData:
    try:
        payload = decode_access_token(token)
        return TokenData(**payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

def get_token_from_cookie(token: str = Cookie(None)) -> str:
    if not token:
        raise HTTPException(status_code=401, detail="Token not found in cookies")
    return token

def get_token_from_header(token: str = Depends(oauth2_scheme)) -> str:
    return token

def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookie)] = None,
    header_token: Annotated[str, Depends(get_token_from_header)] = None
) -> TokenData:
    if token:
        return decode_token(token)
    elif header_token:
        return decode_token(header_token)
    else:
        raise HTTPException(status_code=401, detail="Token not found")

def get_user_by_token(token: str, db) -> TokenData:
    user_id = decode_token(token).user_id
    return db.query(Manager).filter(Manager.id == user_id).first()

user_dep = Annotated[TokenData, Depends(get_current_user)]