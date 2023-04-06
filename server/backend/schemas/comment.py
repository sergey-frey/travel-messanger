from uuid import UUID
from datetime import datetime
from backend.schemas import ContentBase


class CommentBase(ContentBase):
    text: str
    id: int  # added this line
    owner: UUID  # added this line
    content_id: int  # added this line
    created_at: datetime  # added this line
    updated_at: datetime  # added this line


class CommentCreate(CommentBase):   # modified this line
    pass   # modified this line


class CommentUpdate(CommentBase):   # modified this line
    pass   # modified this line


class CommentDelete(CommentBase):   # modified this line
    pass


class Comment(CommentBase):   # modified this line
    pass   # modified this line

    class Config:   # modified this line
        orm_mode = True   # modified this line
