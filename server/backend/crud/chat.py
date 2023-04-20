from sqlalchemy import UUID, delete, insert, select, update

from backend.db.models import Chat
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.db.models import Chat, Message
from backend.dto.chat import ChatUpdate

# Create a new chat instance


async def _create_chat(name, owner, session: AsyncSession):
    query = Chat(name=name, owner=owner)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query

# Query all chats with their associated messages and users


async def _get_chats(session):
    stmt = select(Chat).options(selectinload(
        Chat.messages).selectinload(Message.user))
    result = await session.execute(stmt)
    return result.scalars().all()

# Query one chats


async def get_chat(chat_id, session):
    stmt = select(Chat).where(Chat.id == chat_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def _update_chat(chat_id: UUID, chat: ChatUpdate, session: AsyncSession):
    query = update(Chat).where(Chat.id == chat_id).values(
        name=chat.name).returning(Chat)
    chat_to_update = await session.execute(query)
    update_user_id_row = chat_to_update.fetchone()
    if update_user_id_row:
        await session.commit()
        return update_user_id_row[0]
    await session.refresh(chat_to_update)
    return chat_to_update


async def _delete_chat(chat_id: UUID, session: AsyncSession):
    query = delete(Chat).where(Chat.id == chat_id)
    chat_to_delete = await session.execute(query)
    if chat_to_delete:
        await session.commit()
        return {"message": "chat deleted"}
