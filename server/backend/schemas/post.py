from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel
from backend.schemas import ContentBase
from backend.schemas.comment import Comment




class PostBase(ContentBase):
    title: str
    content: str
    owner: UUID

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    owner: int
    created_at: datetime
    comments: List[Comment] = []

    class Config:
        orm_mode = True