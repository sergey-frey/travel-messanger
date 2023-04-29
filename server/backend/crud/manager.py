import asyncio
from uuid import UUID
from typing import Dict, List
from sqlalchemy import UUID
from backend.app.room import Room, log
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import WebSocket, WebSocketDisconnect
from backend.app.direct import Direct

from backend.crud.chat import (
    group_log_message,
    personal_log_message,
    _add_user_to_chat,
    _kick_user,
)


# TODO: Replace this other segment of code
# await _add_user_to_chat(
#     chat_id, session, sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f"
# )


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
        await self.room.broadcast_user_joined(sender_id)
        self.room.add_user(sender_id, websocket)

        try:
            while True:
                msg = await websocket.receive_text()
                if "/kick" in msg:
                    # await self.room.kick_user(sender_id)
                    sender_id = "ecc966ab-1fea-4a8f-9da2-3524e2f6d55f"
                    await _kick_user(
                        chat_id,
                        sender_id,
                        session,
                    )

                if "/ban" in msg:
                    # await self.room.banned_user(sender_id)
                    pass
                elif receiver_id is not None:
                    await personal_log_message(
                        session,
                        receiver_id,
                        msg,
                        sender_id="ecc966ab-1fea-4a8f-9da2-3524e2f6d55f",
                    )
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


class PersonalConnectionManager:
    def __init__(self, personal_room: Direct):
        self.room = personal_room
        self.active_connections: Dict[UUID, WebSocket] = {}

    async def connect(
        self,
        receiver_id: UUID,
        sender_id: UUID,
        websocket: WebSocket,
        session: AsyncSession,
    ):
        await websocket.accept()
        self.active_connections[sender_id] = websocket

        # Add the sender to the room
        self.room.add_user(sender_id)

        # Send a "user joined" message to the receiver
        receiver_ws = self.active_connections.get(receiver_id)
        if receiver_ws:
            await receiver_ws.send_json(
                {"type": "PERSONAL_JOIN", "data": {"user_id": sender_id}}
            )

    async def send_personal_message(
        self, message: str, sender_id: UUID, receiver_id: UUID
    ):
        # Send a personal message from the sender to the receiver
        receiver_ws = self.active_connections.get(receiver_id)
        if receiver_ws:
            await receiver_ws.send_json(
                {
                    "type": "PERSONAL_MESSAGE",
                    "data": {"message": message, "sender_id": sender_id},
                }
            )

    def disconnect(self, user_id: UUID):
        # Remove the user from the room and close their WebSocket connection
        self.room.remove_user(user_id)
        del self.active_connections[user_id]
