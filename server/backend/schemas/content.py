

from pydantic import BaseModel


class ContentRead(BaseModel):
    pass

    class Config:
        orm_mode = True


class ContentCreate(BaseModel):
    pass


class Photo(ContentCreate):
    src: str


class Post(ContentCreate):
    pass
