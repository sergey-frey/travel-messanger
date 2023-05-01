from fastapi import APIRouter
from . import endpoints
from fastapi.templating import Jinja2Templates

api_router = APIRouter()
api_router.include_router(endpoints.router, prefix="/v1")
