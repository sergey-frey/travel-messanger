import asyncio
from uuid import UUID
from typing import List
from sqlalchemy import UUID
from backend.app.room import Room, log
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket, WebSocketDisconnect

from backend.crud.chat import (
    ban,
    group_log_message,
    kick,
    personal_log_message,
    _add_user_to_chat,
)


class ConnectionManager:
    def __init__(self, room: Room):
        self.room = room
        self.active_connections: List[WebSocket] = []

    async def connect(
        self,
        chat_id: UUID | None,
        receiver_id: UUID | None,
        sender_id: UUID,
        websocket: WebSocket,
        session: AsyncSession,
    ):
        await websocket.accept()
        self.active_connections.append(websocket)
        await websocket.send_json({"type": "ROOM_JOIN", "data": {"user_id": sender_id}})
        """
        Create a session to interact with the database
        Retrieve or create the user object
        Add the user to the room
        """
        # await _add_user_to_chat(
        #     chat_id, session, sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f"
        # )
        await self.room.broadcast_user_joined(sender_id)
        self.room.add_user(sender_id, websocket)

        try:
            while True:
                msg = await websocket.receive_text()
                if "/ban" in msg:
                    await ban(
                        session,
                        chat_id,
                        sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f",
                    )
                    # await self.room.banned_user(sender_id)
                if "/kick" in msg:
                    await kick(
                        session,
                        chat_id,
                        sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f",
                    )
                    # await self.room.banned_user(sender_id)
                elif receiver_id is not None:
                    await personal_log_message(session, receiver_id, msg, sender_id)
                    await self.send_personal_message(msg, self.room._users[receiver_id])
                else:
                    await group_log_message(
                        session,
                        chat_id,
                        msg,
                        sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f",
                    )
                    await self.room.broadcast_message(sender_id, msg)
        except WebSocketDisconnect:
            self.disconnect(websocket)

    def disconnect(self, websocket: WebSocket):
        for sender_id, conn in self.room._users.items():
            if conn == websocket:
                # Remove from active_connections list
                self.active_connections.remove(websocket)
                self.room.remove_user(sender_id)
                asyncio.create_task(self.room.broadcast_user_left(sender_id))
                log.info("The connection is closed.")
                break

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json({"message": message, "sender_ids": self.room._users})

    async def broadcast(self, message: str, sender_ids: List[UUID]):
        for connection in self.active_connections:
            await connection.send_json({"message": message, "sender_ids": sender_ids})
