from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.user import UserRead
from backend.crud import base as crud
from backend.db.models import User
from backend.app.users import current_active_user
from backend.db.database import async_session
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}


@router.get("/", tags=["user"], description="Endpoint for user authentication", response_model=UserRead)
# , exclude={"wrap"}, db: AsyncSession = Depends(async_session)
async def get_user_by_uuid(user_id: UUID) -> UserRead:
    """
    Authenticates a user and returns an access token.
    """
    try:
        return await crud.get_user(user_id)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


# @router.get("/", tags=["user"], description="Endpoint for user authentication", response_model=UserRead)
# async def get_user_by_email(email: str) -> UserRead:
#     """
#     Authenticates a user and returns an access token.
#     """
#     return {"message": "cringe"}
