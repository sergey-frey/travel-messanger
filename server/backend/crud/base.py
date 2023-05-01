import secrets
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.models import User, GroupChat
from backend.dto.user import UserRead
from backend.app.users import current_active_user


async def get_users(session):
    # Query all users
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_user(user_id, session: AsyncSession):
    # Query a specific user by ID
    stmt = select(User).where(User.id == user_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def regenerate_invite_link(chat_id, session):
    # Check if the chat exists
    chat = await select(GroupChat).where(GroupChat.id == chat_id)
    result = await session.execute(chat)
    if chat is None:
        return {"message": f"Chat {chat_id} not found."}

    # Generate a unique invite link using a secure random token
    token = secrets.token_urlsafe(16)
    invite_link = f"http://travel.com/invite/{token}"

    # Update the chat with the new invite link and commit the changes
    chat.invite_link = invite_link
    await session.commit()

    return {"invite_link": invite_link}
