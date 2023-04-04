from fastapi import APIRouter, Depends
from backend.crud.post import create_post, update_post, read_posts
from backend.db.database import get_session
from backend.schemas.post import PostGet, PostCreate, PostDelete, PostUpdate
router = APIRouter()


@router.get("/posts/", response_model=PostGet)
async def create_post(session: AsyncSession = Depends(get_session)):
    return


@router.post("/posts/")
async def get_post(session: AsyncSession = Depends(get_session)):
    pass


@router.put("/posts/{post_id}")
async def update_post(session: AsyncSession = Depends(get_session)):
    pass


@router.delete("/posts/{post_id}")
async def delete_post(session: AsyncSession = Depends(get_session)):
    pass
