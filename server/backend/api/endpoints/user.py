from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request
from backend.dto.user import UserRead
from backend.crud import base as crud
from backend.db.models import User
from backend.app.users import current_active_user
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.room import Room
from backend.dto.chat import UserListResponse

router = APIRouter()


# @router.get("/", description="Endpoint for get user data", response_model=UserRead)
# async def get_user_by_uuid(user_id: UUID, db: AsyncSession = Depends(get_session)) -> UserRead:
#     """
#     Authenticates a user and returns an access token.
#     """
#     try:
#         return await crud.get_user(user_id, db)
#     except HTTPException as exception:
#         raise HTTPException(
#             status_code=503, detail=f"Database error: {exception}")


@router.get("/", response_model=UserListResponse)
async def list_users(request: Request):
    """List all users connected to the room."""
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    return {"users": room.user_list}


@router.get("/{user_id}")
async def get_user_info(request: Request, user_name: str):
    room: Optional[Room] = request.get("room")
    if room is None:
        raise HTTPException(500, detail="Global `Room` instance unavailable!")
    user = room.get_user(user_name)
    if user is None:
        raise HTTPException(404, detail=f"No such user: {user_name}")
    return user
