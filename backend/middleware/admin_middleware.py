from fastapi import FastAPI, Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import RedirectResponse

from core.logging_config import logger
from depends.auth import get_user_by_token
from depends.db import get_db
from schemas import TokenData
from errors.admin import AccessForbiddenException

class AdminMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/admin"):
            try:
                db = next(get_db())
                access_token = request.cookies.get("access_token")
                current_user: TokenData = get_user_by_token(access_token, db=db)
                if not current_user.is_admin:
                    raise AccessForbiddenException()
            except HTTPException as e:
                if e.status_code == 401:
                    # Redirect to login page if token has expired
                    return RedirectResponse(url="/login")
                raise HTTPException(status_code=e.status_code, detail=e.detail)
        
        response = await call_next(request)
        return response