import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from backend.db.models import User, Chat, Message

# Query all users
async def get_users(db):
        stmt = select(User)
        result = await db.execute(stmt)
        return result.scalars().all()

# Query a specific user by ID
async def get_user(user_id, db: AsyncSession):
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        return result.scalars().first()
        
# Query all chats with their associated messages and users
async def get_chats(db):
        stmt = select(Chat).options(selectinload(
            Chat.messages).selectinload(Message.user))
        result = await db.execute(stmt)
        return result.scalars().all()

# Query one chats 
async def get_chat(chat_id,db):
        stmt = select(Chat).where(Chat.id == chat_id)
        result = await db.execute(stmt)
        return result.scalars().first()

# Query the number of messages in a specific chat
async def get_message_count(chat_id,db):
        stmt = select(func.count(Message.id)).where(
            Message.chat_id == chat_id)
        result = await db.execute(stmt)
        return result.scalar()

# Query the most active user (with the most messages)
async def get_most_active_user(db):
        stmt = select(User).join(User.messages).group_by(
            User.id).order_by(func.count(Message.id).desc()).limit(1)
        result = await db.execute(stmt)
        return result.scalars().first()
