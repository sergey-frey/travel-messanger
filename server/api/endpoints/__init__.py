from . import example, chat, auth
from fastapi import APIRouter



router = APIRouter()
router.include_router(
    example.router,
    prefix="/root",
    tags=["root"],
)
router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"],
)
router.include_router(
    auth.router,
    prefix="/auth",
    tags=["auth"],
)
