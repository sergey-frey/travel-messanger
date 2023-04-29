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
    owner_id: UUID
    created_at: datetime  # Added created_at field to the Post model.
    # comments: List[Comment] = []  # Added comments field to the Post model.


class PostCreate(BaseModel):
    title: str
    content: str


class PostUpdate(BaseModel):
    title: str
    content: str


class PostDelete(BaseModel):
    pass


class Post(PostBase):
    pass

    class Config:
        orm_mode = True
