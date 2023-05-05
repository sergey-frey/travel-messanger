from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from backend.crud.post import _create_post, _update_post, _read_posts, _delete_post
from backend.db.database import get_session
from backend.dto.user import UserRead
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user
from backend.dto.post import UserPost, UserPostCreate, UserPostUpdate

router = APIRouter()


@router.post("/user/", response_model=UserPost)
async def user_create_post(
    post: UserPostCreate,
    current_user: UserRead = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
) -> UserPostCreate:
    try:
        return await _create_post(post, current_user.id, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.get("/user/", response_model=List[UserPost])
async def user_get_posts(
    skip: int = 0, limit: int = 5, session: AsyncSession = Depends(get_session)
) -> List[UserPost]:
    try:
        return await _read_posts(skip, limit, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.put("/user/{post_id}", response_model=UserPost)
async def user_update_post(
    post_id, post: UserPostUpdate, session: AsyncSession = Depends(get_session)
) -> UserPost:
    try:
        return await _update_post(post_id, post, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")


@router.delete("/user/{post_id}")
async def user_delete_post(
    post_id: UUID, session: AsyncSession = Depends(get_session)
) -> dict:
    try:
        return await _delete_post(post_id, session)
    except HTTPException as error:
        raise HTTPException(status_code=404, detail=f"Post not found as {error}")
