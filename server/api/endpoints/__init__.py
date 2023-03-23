from . import example
from fastapi import APIRouter


router = APIRouter()
router.include_router(
    example.router,
    prefix="/applications",
    tags=["applications"],
)