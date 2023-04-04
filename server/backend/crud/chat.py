from sqlalchemy import insert, select

from backend.db.models import Chat
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.db.models import Chat, Message

# Create a new chat instance


async def create_chat(name, owner, session: AsyncSession):
    chats = insert(Chat)
    result = await session.execute(chats)
    return result.scalars().all()

# Query all chats with their associated messages and users


async def get_chats(session):
    stmt = select(Chat).options(selectinload(
        Chat.messages).selectinload(Message.user))
    result = await session.execute(stmt)
    return result.scalars().all()

# Query one chats


async def get_chat(chat_id, session):
    stmt = select(Chat).where(Chat.id == chat_id)
    result = await session.execute(stmt)
    return result.scalars().first()
