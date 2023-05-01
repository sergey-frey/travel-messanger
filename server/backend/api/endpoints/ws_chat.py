import uuid
from backend.app.room import Room
from backend.crud.manager import ConnectionManager, PersonalConnectionManager
from backend.app.direct import Direct
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_session


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
    chat_id = "0c6cfc23-1475-4c6a-9864-840b352f260e"
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
