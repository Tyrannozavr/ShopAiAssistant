from fastapi import Body, APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

from depends.db import db_dep
from models import Manager
from services.auth_service import verify_password
from services.token_service import create_access_token
from errors.admin import UserNotFoundException, InvalidCredentialsException

templates = Jinja2Templates(directory="templates")

router = APIRouter()

# Endpoint для отображения формы входа
@router.get("/login")
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Endpoint для обработки данных формы
@router.post("/login")
async def login(
        db: db_dep,
        username: str = Body(),
        password: str = Body(),
):
    find_user = db.query(Manager).filter(Manager.username == username).first()

    if not find_user:
        raise UserNotFoundException()

    if not verify_password(password, find_user.hashed_password):
        raise InvalidCredentialsException()

    access_token = create_access_token(manager=find_user)

    return {"access_token": access_token}