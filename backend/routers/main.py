from fastapi import APIRouter

from . import admin
from . import auth
# import config
from . import manager

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(manager.router, prefix="/manager", tags=["Manager"])
# router.include_router(config.router, prefix="/config", tags=["Config"])