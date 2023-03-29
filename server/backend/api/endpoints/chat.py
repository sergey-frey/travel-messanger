import datetime
# from . import templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, WebSocket
from backend.db.models import Chat, User, Message
from backend.crud.base import get_chat, get_user

router = APIRouter()
connected_websockets = set()


@router.websocket('/ws/{chat_id}/{user_id}')
# , session: AsyncSession = Depends(async_session)
async def chat_ws(websocket: WebSocket, chat_id: int, user_id: int):
    # Accept the websocket connection
    await websocket.accept()

    # Add the websocket to the set of connected websockets
    connected_websockets.add(websocket)

    # Retrieve the chat and user objects from the database
    chat = get_chat(chat_id)
    user = get_user(user_id)

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


@router.get('/')
async def home():
    chats = session.query(Chat).all()
    return templates.TemplateResponse('index.html', {'request': None, 'chats': chats})


@router.get('/chat/{chat_id}/{user_id}', response_class=HTMLResponse)
async def chat(request, chat_id: int, user_id: int):
    # Retrieve the chat and user objects from the database
    chat = session.query(Chat).filter_by(id=chat_id).first()
    user = session.query(User).filter_by(id=user_id).first()
    return templates.TemplateResponse('chat.html', {'request': request, 'chat': chat, 'user': user})
