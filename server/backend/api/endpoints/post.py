from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from backend.crud.post import _create_post, _update_post, _read_posts, _delete_post
from backend.db.database import get_session
from backend.dto.post import PostCreate, PostDelete, PostUpdate, Post
from backend.dto.user import UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user

router = APIRouter()


@router.post("/posts/", response_model=Post)
async def create_post(
    post: PostCreate,
    current_user: UserRead = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
) -> PostCreate:
    try:
        return await _create_post(post, current_user.id, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.get("/posts/", response_model=List[Post])
async def get_posts(
    skip: int = 0, limit: int = 5, session: AsyncSession = Depends(get_session)
) -> List[Post]:
    try:
        return await _read_posts(skip, limit, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(
    post_id, post: PostUpdate, session: AsyncSession = Depends(get_session)
) -> Post:
    try:
        return await _update_post(post_id, post, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.delete("/posts/{post_id}")
async def delete_post(
    post_id: UUID, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        return await _delete_post(post_id, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")
