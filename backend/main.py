from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from core.logging_config import logger  # Import the logger

# Example usage
from middleware.admin_middleware import AdminMiddleware
from routers import main as main_router, admin as admin_router
from seed.admin import seed_admin_user
from services.admin import admin

load_dotenv()  # Load environment variables from .env file

app = FastAPI(docs_url=None, redoc_url=None)
admin.mount_to(app)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(AdminMiddleware)
app.include_router(main_router.router, prefix="/api")
app.include_router(admin_router.router, tags=["Admin"])

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    logger.info("Custom Swagger UI HTML called")
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


@app.on_event("startup")
async def on_startup():
    seed_admin_user()

# Include your routers and other setup here