from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from schemas import TokenData
from services.token_service import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user_by_token(token: str = Depends(oauth2_scheme)) -> TokenData:
    try:
        payload = decode_access_token(token)
        return TokenData(**payload)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))