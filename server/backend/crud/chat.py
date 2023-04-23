import asyncio
from typing import List
from sqlalchemy import UUID, delete, insert, select, update

from backend.db.models import Chat
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from backend.db.models import Chat, Message
from backend.dto.chat import ChatUpdate
from uuid import UUID
from backend.dto.chat import ChatUpdate
from fastapi import WebSocket, WebSocketDisconnect
from backend.app.room import Room
from backend.dto.user import UserRead
from backend.db.models import UserChat
from sqlalchemy import and_

from backend.db.models import UserChatBans


class ConnectionManager:
    def __init__(self, room: Room):
        self.room = room
        self.active_connections: List[WebSocket] = []

    async def connect(self, chat_id, user_id, websocket: WebSocket, session: AsyncSession):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_json({"type": "ROOM_JOIN", "data": {"user_id": user_id}})
        print(self.room._users)
        """
        Create a session to interact with the database
        Retrieve or create the user object
        Add the user to the room
        """
        stmt = select(UserChat).where(
            and_(UserChat.c.user_id == user_id, UserChat.c.chat_id == chat_id)
        )
        if stmt is None:
            room = Room(id=self.room.id)
            session.add(room)
        # self.room.add_user(user_id, websocket)
        await session.commit()
        await self.room.broadcast_user_joined(user_id)
        self.room.add_user(user_id, websocket)

        try:
            while True:
                msg = await websocket.receive_text()
                await log_message(session,  chat_id, msg, user_id="514fed45-a776-4e17-82b5-6ef0f30a91ba")
                await self.room.broadcast_message(user_id, msg)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        for user_id, conn in self.room._users.items():
            if conn == websocket:
                # Remove from active_connections list
                self.active_connections.remove(websocket)
                self.room.remove_user(user_id)
                asyncio.create_task(self.room.broadcast_user_left(user_id))
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"message": message, "user_ids": self.room._users})

    async def broadcast(self, message: str, user_ids: List[UUID]):
        for connection in self.active_connections:
            await connection.send_json({"message": message, "user_ids": user_ids})

# Define the log function


async def log_message(session, chat_id,  msg: str, user_id,):
    # Wait for the specified delay before logging the message
    # Open a new database session
    # Create a new message log entry
    log_entry = Message(text=msg, user_id=user_id, chat_id=chat_id)
    session.add(log_entry)
    await session.commit()
    await session.refresh(log_entry)


async def kick(user_id, chat_id, session):
    stmt = delete(UserChat).where(
        and_(UserChat.c.user_id == user_id, UserChat.c.chat_id == chat_id))
    await session.execute(stmt)
    await session.commit()
    return {"message": f"User {user_id} was kicked."}


async def ban(user_id, chat_id, session):
    # Check if the user is already banned
    stmt = select(UserChatBans).where(
        and_(UserChatBans.c.user_id == user_id,
             UserChatBans.c.chat_id == chat_id)
    )
    result = await session.execute(stmt)
    already_banned = result.fetchone() is not None

    if not already_banned:
        # Add a new ban record
        stmt = UserChatBans.insert().values(user_id=user_id, chat_id=chat_id)
        await session.execute(stmt)
        await session.commit()
        return {"message": f"User {user_id} was banned from chat {chat_id}."}
    else:
        return {"message": f"User {user_id} is already banned from chat {chat_id}."}


async def _add_user_to_chat(user_id, chat_id):
    query = insert(UserChat).values(user_id, chat_id)
    result = await query.execute()
    return result.scalars().first()


async def _create_chat(name, owner, session: AsyncSession):
    """Create a new chat instance"""
    query = Chat(name=name, owner=owner)
    session.add(query)
    await session.commit()
    await session.refresh(query)
    return query


async def _get_chats(session):
    """Query all chats with their associated messages and users"""
    stmt = select(Chat).options(selectinload(
        Chat.messages).selectinload(Message.user))
    result = await session.execute(stmt)
    return result.scalars().all()


async def _get_chat(chat_id, session):
    """Query one chats"""
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
