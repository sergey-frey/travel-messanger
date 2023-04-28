from typing import Any, Optional
from uuid import UUID
import uuid
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
from backend.crud.manager import ConnectionManager

router = APIRouter()

room = Room()
manager = ConnectionManager(room)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, session: AsyncSession = Depends(get_session)
):
    current_user = str(uuid.uuid4())
    chat_id = "6e5ef0d7-c563-42aa-a513-4e1cd88a7ee3"
    # receiver_id = "8805d0e6-f627-4e61-baab-409aa8d7d490"
    await manager.connect(chat_id, None, current_user, websocket, session)


# @router.websocket("/ws/personal_chat/{receiver_id}")
# async def websocket_endpoint_personal_messege(
#     websocket: WebSocket,
#     sender_id: str,
#     receiver_id: str,
#     session: AsyncSession = Depends(get_session),
# ):
#     await manager.connect(
#         session, websocket, sender_id=sender_id, receiver_id=receiver_id
#     )


# @router.websocket("/ws/moderator")
# async def websocket_moderator_endpoint(websocket: WebSocket,
#                                        chat_info: dict = Depends(chat_info_vars)):
#     # check the user is allowed into the chat room
#     # verified = await verify_user_for_room(chat_info)
#     # open connection

#     if not chat_info['username'] == 'moderator':
#         print('failed verification')
#         await websocket.close()
#         return

#     await websocket.accept()
#     # spin up coro's for inbound and outbound communication over the socket
#     await asyncio.gather(ws_send_moderator(websocket, chat_info))


@router.post("/")
async def create_chat(
    name: str,
    owner: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _create_chat(name, owner.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.get("/")
async def get_all_chats(session: AsyncSession = Depends(get_session)):
    try:
        return await _get_chats(session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.put("/")
async def update_chats(
    chat_id: UUID, chat: ChatUpdate, session: AsyncSession = Depends(get_session)
):
    try:
        return await _update_chat(chat_id, chat, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.delete("/")
async def delete_chat(chat_id: UUID, session: AsyncSession = Depends(get_session)):
    try:
        return await _delete_chat(chat_id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")
