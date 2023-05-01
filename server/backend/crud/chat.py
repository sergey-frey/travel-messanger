import secrets
from uuid import UUID
from sqlalchemy import UUID, delete, insert, select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.dto.chat import ChatUpdate
from backend.db.models import (
    GroupChat,
    GroupMessage,
    PersonalChat,
    PersonalMessage,
    UserChatBans,
    UserChatMember,
)


async def group_log_message(session, chat_id, msg: str, sender_id):
    """Wait for the specified delay before logging the message
    Open a new database session
    Create a new message log entry"""
    log_entry = GroupMessage(text=msg, sender_id=sender_id, chat_id=chat_id)
    session.add(log_entry)
    await session.commit()
    await session.refresh(log_entry)


async def personal_log_message(session, receiver_id, msg: str, sender_id):
    """Wait for the specified delay before logging the message
    Open a new database session
    Create a new message log entry"""
    log_entry = PersonalMessage(text=msg, sender_id=sender_id, receiver_id=receiver_id)
    session.add(log_entry)
    await session.commit()
    await session.refresh(log_entry)


async def _if_user_is_banned(user_id, chat_id, session):
    stmt = select(UserChatBans).where(
        and_(UserChatBans.c.user_id == user_id, UserChatBans.c.chat_id == chat_id)
    )
    rows = await session.execute(stmt)
    result = rows.fetchone()
    return result


async def _kick_user(chat_id, user_id, session):
    stmt = delete(UserChatMember).where(
        and_(UserChatMember.c.user_id == user_id, UserChatMember.c.chat_id == chat_id)
    )
    await session.execute(stmt)
    await session.commit()
    return {"message": f"User {user_id} was kicked."}


async def _ban(chat_id, user_id, session: AsyncSession):
    # Check if the user is already banned
    if _if_user_is_banned is None:
        # Add a new ban record
        await _kick_user(chat_id, user_id, session)
        stmt = insert(UserChatBans).values(user_id=user_id, chat_id=chat_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": "забанен нахуй"}
        # return {"message": f"User {user_id} was banned from chat {chat_id}."}
    else:
        return {"message": "пока живет"}
        # return {"message": f"User {user_id} is already banned from chat {chat_id}."}


async def _unban(chat_id, user_id, session: AsyncSession):
    if _if_user_is_banned:
        stmt = delete(UserChatBans).where(
            UserChatBans.c.user_id == user_id, UserChatBans.c.chat_id == chat_id
        )
        await session.execute(stmt)
        await session.commit()
        return {"message": "попросил o пощаде"}
    else:
        return {"message": "Хвалит небеса за то что уже разбанен"}


async def _add_user_to_chat(chat_id, session, sender_id):
    stmt = select(UserChatMember).where(
        and_(UserChatMember.c.user_id == sender_id, UserChatMember.c.chat_id == chat_id)
    )
    if stmt is None:
        query = UserChatMember(user_id=sender_id, chat_id=chat_id)
        session.add(query)
        await session.commit()
        await session.refresh(query)
    return stmt


async def _create_group_chat(name, owner, session: AsyncSession):
    """Create a new chat instance"""
    token = secrets.token_urlsafe(16)
    invite_link = f"http://travel.com/invite/{token}"
    query = GroupChat(name=name, owner=owner, invite_link=invite_link)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query


async def _create_personal_chat(sender_id, receiver_id, session: AsyncSession):
    """Create a new personal chat"""
    query = PersonalChat(sender_id=sender_id, receiver_id=receiver_id)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query


async def _get_chats(session):
    """Query all chats with their associated messages and users"""
    stmt_personal_chat = select(PersonalChat).options(
        selectinload(PersonalChat.sender), selectinload(PersonalChat.receiver)
    )
    stmt_group_chat = select(GroupChat).options(
        selectinload(GroupChat.messages).selectinload(GroupMessage.user)
    )
    stmt = stmt_personal_chat.union_all(stmt_group_chat)
    result = await session.execute(stmt)
    return result.scalars().all()


async def _get_chat(chat_id, session):
    """Query one chats"""
    stmt = select(GroupChat).where(GroupChat.id == chat_id)
    result = await session.execute(stmt)
    return result.scalars().first()


async def _update_chat(chat_id: UUID, chat: ChatUpdate, session: AsyncSession):
    query = (
        update(GroupChat)
        .where(GroupChat.id == chat_id)
        .values(name=chat.name)
        .returning(GroupChat)
    )
    chat_to_update = await session.execute(query)
    update_user_id_row = chat_to_update.fetchone()
    if update_user_id_row:
        await session.commit()
        return update_user_id_row[0]
    await session.refresh(chat_to_update)
    return chat_to_update


async def _delete_chat(chat_id: UUID, session: AsyncSession):
    query = delete(GroupChat).where(GroupChat.id == chat_id)
    chat_to_delete = await session.execute(query)
    if chat_to_delete:
        await session.commit()
        return {"message": "chat deleted"}
