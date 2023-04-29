import asyncio
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql import func
from backend.db.models import User


# Query all users
async def get_users(session):
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


# Query a specific user by ID


async def get_user(user_id, session: AsyncSession):
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def if_user_in_chat_bans(user_id, session: AsyncSession):
    pass


# Query the number of messages in a specific chat
# async def get_message_count(chat_id, session):
#     stmt = select(func.count(Message.id)).where(
#         Message.chat_id == chat_id)
#     result = await session.execute(stmt)
#     return result.scalar()

# Query the most active user (with the most messages)


# async def get_most_active_user(session):
#     stmt = select(User).join(User.messages).group_by(
#         User.id).order_by(func.count(Message.id).desc()).limit(1)
#     result = await session.execute(stmt)
#     return result.scalars().first()
