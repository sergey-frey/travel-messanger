from fastapi import APIRouter


router = APIRouter()


@router.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome"}
