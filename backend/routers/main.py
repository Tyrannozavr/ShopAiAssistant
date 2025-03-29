from fastapi import APIRouter

from . import admin, chatgpt
from . import auth
from . import manager
from . import orders  # Import the orders router

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(manager.router, prefix="/manager", tags=["Manager"])
router.include_router(orders.router, prefix="/orders", tags=["Orders"])  # Include the orders router
router.include_router(chatgpt.router, prefix="/chatgpt", tags=["ChatGPT"])  # Include the chatgpt router
