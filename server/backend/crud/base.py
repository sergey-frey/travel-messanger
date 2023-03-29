import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from backend.db.models import User, Chat, Message
from backend.db.database import get_session


# Query all users
async def get_users():
    async with get_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        return result.scalars().all()

# Query a specific user by ID
async def get_user(user_id, db: AsyncSession):
    async with db as session:
        stmt = select(User).where(User.id == user_id)
        result = await session.execute(stmt)
        return result.scalars().first()
        
# Query all chats with their associated messages and users
async def get_chats():
    async with get_session() as session:
        stmt = select(Chat).options(selectinload(
            Chat.messages).selectinload(Message.user))
        result = await session.execute(stmt)
        return result.scalars().all()

# Query one chats 
async def get_chat(chat_id):
    async with get_session() as session:
        stmt = select(Chat).where(Chat.id == chat_id)
        result = await session.execute(stmt)
        return result.scalars().first()

# Query the number of messages in a specific chat
async def get_message_count(chat_id):
    async with get_session() as session:
        stmt = select(func.count(Message.id)).where(
            Message.chat_id == chat_id)
        result = await session.execute(stmt)
        return result.scalar()

# Query the most active user (with the most messages)
async def get_most_active_user():
    async with get_session() as session:
        stmt = select(User).join(User.messages).group_by(
            User.id).order_by(func.count(Message.id).desc()).limit(1)
        result = await session.execute(stmt)
        return result.scalars().first()
