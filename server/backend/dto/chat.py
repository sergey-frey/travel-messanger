from typing import List, Optional
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


class ChatBase(BaseModel):
    id: UUID  # Added id field to the Chat model.
    title: str
    content: str
    owner_id: UUID
    created_at: datetime  # Added created_at field to the Chat model.
    # comments: List[Comment] = []  # Added comments field to the Chat model.


class ChatCreate(BaseModel):
    title: str
    content: str


class ChatUpdate(BaseModel):
    name: str
    avatar: Optional[str]


class ChatDelete(BaseModel):
    pass


class Chat(ChatBase):
    pass

    class Config:
        orm_mode = True
