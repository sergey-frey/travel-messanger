from typing import Any, Optional
from uuid import UUID
from backend.crud.chat import _create_chat, _delete_chat, _update_chat, _get_chats
from backend.dto.chat import ChatUpdate
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect

from backend.app.room import Room, log
from backend.dto.user import UserRead
from starlette.endpoints import WebSocketEndpoint
from backend.dto.user import UserRead
from backend.crud.chat import ConnectionManager

router = APIRouter()
# Homepage with a form to join a chat
room = Room()
manager = ConnectionManager(room)


async def get_current_user(websocket: WebSocket, user=Depends(current_active_user)):
    return user

# , current_user=Depends(get_current_user)


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, session: AsyncSession = Depends(get_session)):
    chat_id = "45d5725d-09b5-48e2-bb88-1321ea9306f1"
    current_user = "b23f9eaf-6318-4e3d-b4e6-d0a1cc9d012e"
    await manager.connect(chat_id, current_user, websocket, session)

# @router.websocket("/ws")
# async def websocket_endpoint(websocket: WebSocket):
#     """Live connection to the global `Room` instance, via WebSocket."""

#     log.info("Connecting new user...")
#     room: Optional[Room] = websocket.scope.get("room")
#     if room is None:
#         raise RuntimeError(f"Global `Room` instance unavailable!")
#     user_id = "Adolf Hitler"  # You need to assign a user ID here
#     await websocket.accept()
#     await websocket.send_json({"type": "ROOM_JOIN", "data": {"user_id": user_id}})
#     await room.broadcast_user_joined(user_id)
#     room.add_user(user_id, websocket)

#     try:
#         while True:
#             msg = await websocket.receive_text()
#             await room.broadcast_message(user_id, msg)
#     except WebSocketDisconnect:
#         room.remove_user(user_id)
#         await room.broadcast_user_left(user_id)
# @router.websocket_route("/ws", name="ws")
# class RoomLive(WebSocketEndpoint):
#     """Live connection to the global :class:`~.Room` instance, via WebSocket."""

#     encoding: str = "text"

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.room: Optional[Room] = None
#         self.user_id: Optional[str] = None
#         self.current_user = None

#     @classmethod
#     def get_next_user_id(cls):
#         """Returns monotonically increasing numbered usernames in the form
#         'user_[number]'
#         """
#         current_user = "xxx"
#         user_id: str = f"Adolf Hitler"
#         return user_id

#     async def on_connect(self, websocket):
#         """Handle a new connection.

#         New users are assigned a user ID and notified of the room's connected
#         users. The other connected users are notified of the new user's arrival,
#         and finally the new user is added to the global :class:`~.Room` instance.
#         """
#         log.info("Connecting new user...")
#         room: Optional[Room] = self.scope.get("room")
#         if room is None:
#             raise RuntimeError(f"Global `Room` instance unavailable!")
#         self.room = room
#         self.user_id =
#         await websocket.accept()
#         await websocket.send_json(
#             {"type": "ROOM_JOIN", "data": {"user_id": self.user_id}}
#         )
#         await self.room.broadcast_user_joined(self.user_id)
#         self.room.add_user(self.user_id, websocket)

#     async def on_disconnect(self, _websocket: WebSocket, _close_code: int):
#         """Disconnect the user, removing them from the :class:`~.Room`, and
#         notifying the other users of their departure.
#         """
#         if self.user_id is None:
#             raise RuntimeError(
#                 "RoomLive.on_disconnect() called without a valid user_id"
#             )
#         self.room.remove_user(self.user_id)
#         await self.room.broadcast_user_left(self.user_id)

#     async def on_receive(self, _websocket: WebSocket, msg: Any):
#         """Handle incoming message: `msg` is forwarded straight to `broadcast_message`."""
#         if self.user_id is None:
#             raise RuntimeError(
#                 "RoomLive.on_receive() called without a valid user_id")
#         if not isinstance(msg, str):
#             raise ValueError(
#                 f"RoomLive.on_receive() passed unhandleable data: {msg}")
#         await self.room.broadcast_message(self.user_id, msg)


@ router.post("/")
async def create_chat(
    name: str,
    owner: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _create_chat(name, owner.id, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@ router.get("/")
async def get_all_chats(session: AsyncSession = Depends(get_session)):
    try:
        return await _get_chats(session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@ router.put("/")
async def update_chats(
    chat_id: UUID, chat: ChatUpdate, session: AsyncSession = Depends(get_session)
):
    try:
        return await _update_chat(chat_id, chat, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@ router.delete("/")
async def delete_chat(chat_id: UUID, session: AsyncSession = Depends(get_session)):
    try:
        return await _delete_chat(chat_id, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")
