

from pydantic import BaseModel


class Content(BaseModel):
    pass


class Photo(Content):
    src: str


class Post(Content):
    pass
