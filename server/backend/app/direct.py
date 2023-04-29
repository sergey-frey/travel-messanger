from typing import Dict
from uuid import UUID

from fastapi import WebSocket

from backend.dto.chat import UserInfo
from backend.app.room import log


class Direct:
    """Personal messaging room state, comprising connected users."""

    def __init__(self):
        self._users: Dict[UUID, WebSocket] = {}
        self._user_meta: Dict[UUID, UserInfo] = {}

    async def send_message(self, sender_id: UUID, receiver_id: UUID, message: str):
        """Send a message from the sender to the receiver."""
        if sender_id not in self._users:
            raise ValueError(f"User {sender_id} is not connected to the room")
        if receiver_id not in self._users:
            raise ValueError(f"User {receiver_id} is not connected to the room")
        log.info("Sending message from %s to %s", sender_id, receiver_id)
        await self._users[receiver_id].send_json(
            {
                "sender_id": str(sender_id),
                "receiver_id": str(receiver_id),
                "message": message,
            }
        )
        self._user_meta[sender_id].message_count += 1
        self._user_meta[receiver_id].message_count += 1

    def get_user_meta(self, user_id: UUID) -> UserInfo:
        """Return user metadata for a given user ID."""
        if user_id not in self._users:
            raise ValueError(f"User {user_id} is not connected to the room")
        return self._user_meta[user_id]
