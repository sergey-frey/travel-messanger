from typing import Dict, List, Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class UserInfo(BaseModel):
    """Chatroom user metadata."""

    user_id: UUID
    connected_at: float
    message_count: int


class UserListResponse(BaseModel):
    """Response model for /list_users endpoint."""

    users: List[UUID]


class GroupChatBase(BaseModel):
    id: UUID  # Added id field to the Chat model.
    name: str
    owner: UUID
    avatar: Optional[str]
    created_at: datetime  # Added created_at field to the Chat model.


class GroupChatCreate(BaseModel):
    name: str
    avatar: Optional[str]


class GroupChatUpdate(BaseModel):
    name: str
    avatar: Optional[str]


class GroupChatDelete(BaseModel):
    pass


class GroupChat(GroupChatBase):
    pass

    class Config:
        orm_mode = True
