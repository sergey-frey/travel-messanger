import datetime
from uuid import UUID
# from . import templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from sqlalchemy import insert, select
from backend.crud import chat,base
from backend.db.models import Chat, User, Message
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user

router = APIRouter()
connected_websockets = set()


@router.websocket('/ws/{chat_id}/{user_id}')
async def chat_ws(websocket: WebSocket, chat_id: int, user_id: int, session: AsyncSession = Depends(get_session)):
    # Accept the websocket connection
    await websocket.accept()

    # Add the websocket to the set of connected websockets
    connected_websockets.add(websocket)

    # Retrieve the chat and user objects from the database
    chat = chat.get_chat(chat_id)
    user = base.get_user(user_id)

    # Loop to receive and broadcast messages
    while True:
        message = await websocket.receive_text()
        now = datetime.utcnow()
        message_obj = Message(text=message, chat=chat,
                              user=user, created_at=now)
        session.add(message_obj)
        session.commit()

        # Broadcast the message to all connected websockets in the chat
        for ws in connected_websockets:
            if ws != websocket:
                await ws.send_text(f'{user.name}: {message}')


# Homepage with a form to join a chat


@router.post('/')
async def create_chat(name: str, owner: UUID = Depends(current_active_user), session: AsyncSession = Depends(get_session)):
    try:
        return await chat.create_chat(name, owner.id, session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")


@router.get('/')
async def get_us(owner: UUID = Depends(current_active_user)):
    return await owner.id


@router.get('/')
async def get_all_chats(session: AsyncSession = Depends(get_session)):
    try:
        return await chat.get_chats(session)
    except HTTPException as exception:
        raise HTTPException(
            status_code=503, detail=f"Database error: {exception}")