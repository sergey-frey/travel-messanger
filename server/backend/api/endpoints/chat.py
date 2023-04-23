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
    current_user = str(uuid.uuid4())
    await manager.connect(chat_id, current_user, websocket, session)


@router.post("/")
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


@router.get("/")
async def get_all_chats(session: AsyncSession = Depends(get_session)):
    try:
        return await _get_chats(session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@router.put("/")
async def update_chats(
    chat_id: UUID, chat: ChatUpdate, session: AsyncSession = Depends(get_session)
):
    try:
        return await _update_chat(chat_id, chat, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@router.delete("/")
async def delete_chat(chat_id: UUID, session: AsyncSession = Depends(get_session)):
    try:
        return await _delete_chat(chat_id, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")
