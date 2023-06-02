from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from backend.dto import ContentBase
from backend.dto.comment import Comment


class PostBase(ContentBase):
    id: UUID  # Added id field to the Post model.
    title: str
    content: str
    created_at: datetime  # Added created_at field to the Post model.


class UserPostCreate(BaseModel):
    title: str
    content: str


class UserPostUpdate(BaseModel):
    title: str
    content: str


class UserPostDelete(BaseModel):
    pass


class UserPost(PostBase):
    post_id: UUID
    user_id: UUID

    class Config:
        orm_mode = True


class CommunityPostCreate(BaseModel):
    title: str
    content: str


class CommunityPostUpdate(BaseModel):
    title: str
    content: str


class CommunityPostDelete(BaseModel):
    pass


class CommunityPost(PostBase):
    post_id: UUID
    community_id: UUID

    class Config:
        orm_mode = True
