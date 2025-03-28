import os
import logging
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from middleware.admin_middleware import AdminMiddleware
from models import Manager, City
from depends.db import get_db
from routers import admin
from routers import main
from services.auth_service import get_hashed_password

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(docs_url=None, redoc_url=None)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(AdminMiddleware)
app.include_router(main.router, prefix="/api")
app.include_router(admin.router, prefix="/admin", tags=["Admin"])

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    logger.info("Custom Swagger UI HTML called")  # Use logging instead of print
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )

def seed_admin_user():
    db_session = next(get_db())
    admin_user = db_session.query(Manager).filter(Manager.is_admin == True).first()
    if not admin_user:
        admin_username = os.getenv("ADMIN_USERNAME")
        admin_password = os.getenv("ADMIN_PASSWORD")
        city = City(name="AdminCity")
        if admin_username and admin_password:
            hashed_password = get_hashed_password(admin_password)
            new_admin = Manager(
                username=admin_username,
                hashed_password=hashed_password,
                city=city,  # You can set a default city or make it configurable
                is_staff=True,
                is_admin=True
            )
            db_session.add(new_admin)
            db_session.commit()
    db_session.close()

@app.on_event("startup")
async def on_startup():
    seed_admin_user()

# Include your routers and other setup here