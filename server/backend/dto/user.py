from typing import Any, Callable, Optional
import uuid

from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[int]):
    id: uuid.UUID
    email: str
    avatar: Optional[str]
    username: str
    role_id: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    wrap: Optional[Callable[..., Any]] = Field(default=None, alias="_")

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    username: str
    avatar: Optional[str]
    email: str
    password: str
    role_id: int
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    avatar: Optional[str]
    email: str
    password: str
    role_id: int
    is_active: Optional[bool]
    is_superuser: Optional[bool]
    is_verified: Optional[bool]
