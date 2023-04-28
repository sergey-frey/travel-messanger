from typing import Optional
from pydantic import BaseModel


class ContentBase(BaseModel):
    likes: Optional[int] = 0
    dislikes: Optional[int] = 0
