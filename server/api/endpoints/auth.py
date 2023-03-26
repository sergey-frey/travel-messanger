from fastapi import APIRouter


router = APIRouter()

@router.get("/", tags=["auth"])
async def authorize() -> dict:
    return {"message": "cringe"}

