import faust
from kafka.app import app
from typing import TypeVar
from mode.utils.futures import stampede

T = TypeVar("T")


class MyModel(faust.Record):
    x: int


channel = app.channel(value_type=MyModel)


class Channel(faust.ChannelT[T]):
    @stampede
    async def maybe_declare(self) -> None:
        """Declare/create this channel, but only if it doesn't exist."""
        ...
