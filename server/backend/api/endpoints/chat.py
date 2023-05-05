from typing import Dict, List
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
    _unban,
    _add_user_to_chat,
)

from backend.dto.chat import GroupChatUpdate, GroupChat
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user
from fastapi import APIRouter, Depends, HTTPException

from backend.crud.base import regenerate_invite_link

router = APIRouter()


# @router.update("/ansable")
# async def regenerate_invite_link():
#     try:
#         return await regenerate_invite_link()
#     except HTTPException as exception:
#         raise HTTPException(
#             status_code=503, detail=f"Database error: {exception}")


@router.get("/")
async def get_all_chats(
    user_id: UUID = Depends(current_active_user),
    session: AsyncSession = Depends(get_session),
) -> List[UUID]:
    try:
        return await _get_chats(user_id.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.put("/", response_model=GroupChat)
async def update_chats(
    chat_id: UUID, chat: GroupChatUpdate, session: AsyncSession = Depends(get_session)
) -> GroupChatUpdate:
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


@router.post("/banned")
async def ban_user_from_chat(
    chat_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _ban(chat_id, user_id.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")


@router.delete("/kick")
async def kick_user_from_chat(
    chat_id: UUID,
    user_id: UUID,
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


@router.delete("/unbanned")
async def unban_user_from_chat(
    chat_id: UUID,
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
):
    try:
        return await _unban(chat_id, user_id.id, session)
    except HTTPException as exception:
        raise HTTPException(status_code=503, detail=f"Database error: {exception}")
