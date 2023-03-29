from backend.db import settings
from contextlib import asynccontextmanager
from typing import Any, AsyncContextManager, AsyncGenerator, Callable
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from backend.utils.base import Base


AsyncSessionGenerator = AsyncGenerator[AsyncSession, None]


async def create_database(url: str) -> None:
    engine = create_async_engine(
        url,
        pool_pre_ping=True,
        future=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


def async_session(
    url: str,
    *,
    wrap: Callable[..., Any] | None = None,
) -> Callable[..., AsyncSessionGenerator] | AsyncContextManager[Any]:
    engine = create_async_engine(
        url,
        pool_pre_ping=True,
        future=True,
    )
    factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        autoflush=False,
        expire_on_commit=False,
    )

    async def get_session() -> AsyncSessionGenerator:  # noqa: WPS430, WPS442
        async with factory() as session:
            yield session

    return get_session if wrap is None else wrap(get_session)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        
override_session = get_session, async_session(settings.DATABASE_URI)
context_session = async_session(
    settings.DATABASE_URI, wrap=asynccontextmanager)
