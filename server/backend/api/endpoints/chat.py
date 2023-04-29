import uuid
from uuid import UUID
from backend.crud.chat import (
    _create_group_chat,
    _delete_chat,
    _update_chat,
    _get_chats,
    _create_personal_chat,
    _kick_user,
    _ban,
    _add_user_to_chat,
)
from backend.dto.chat import ChatUpdate
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user
from fastapi import APIRouter, Depends, HTTPException, WebSocket

from backend.app.room import Room
from backend.crud.manager import ConnectionManager, PersonalConnectionManager
from backend.app.direct import Direct

router = APIRouter()

room = Room()
personal_room = Direct()
manager = ConnectionManager(room)
personal_manager = PersonalConnectionManager(personal_room)


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, session: AsyncSession = Depends(get_session)
):
    current_user = str(uuid.uuid4())
    chat_id = "6e5ef0d7-c563-42aa-a513-4e1cd88a7ee3"
    # receiver_id = "8805d0e6-f627-4e61-baab-409aa8d7d490"
    await manager.connect(chat_id, None, current_user, websocket, session)


@router.websocket("/ws/personal_chat/{receiver_id}")
async def websocket_endpoint_personal_messege(
    websocket: WebSocket,
    sender_id: str,
    receiver_id: str,
    session: AsyncSession = Depends(get_session),
):
    await personal_manager.connect(
        session, websocket, sender_id=sender_id, receiver_id=receiver_id
    )


@router.post("/group_chat")
async def create_group_chat(
    name: str,
    owner: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _create_group_chat(name, owner.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.post("/personal_chat")
async def create_personal_chat(
    receiver_id: UUID = "8805d0e6-f627-4e61-baab-409aa8d7d490",
    sender_id: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _create_personal_chat(sender_id.id, receiver_id, session)
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


@router.delete("/")
async def kick_user_from_chat(
    chat_id: UUID,
    user_id: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _kick_user(
            chat_id,
            user_id.id,
            session,
        )
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.post("/banned")
async def ban_user_from_chat(
    chat_id: UUID,
    user_id: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _ban(chat_id, user_id.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.delete("/unbanned")
async def unban_user_from_chat(
    chat_id: UUID,
    user_id: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _unban(chat_id, user_id.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")
