from uuid import UUID
from datetime import datetime
from backend.schemas import ContentBase


class CommentBase(ContentBase):
    text: str


class CommentCreate(CommentBase):
    pass


class Comment(CommentBase):
    id: int
    owner: UUID
    content_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
