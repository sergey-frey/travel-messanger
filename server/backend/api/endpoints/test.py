from fastapi import APIRouter
import datetime
from uuid import UUID
from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from sqlalchemy import insert, select
from backend.crud import chat, base
from backend.db.models import Chat, User, Message
from backend.db.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.users import current_active_user
from typing import Set


router = APIRouter()
connected_websockets: Set[WebSocket] = set()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/niger")
async def get():
    return HTMLResponse(html)


@router.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")


@router.websocket('/ws/{chat_id}/{user_id}')
async def chat_ws(
    websocket: WebSocket,
    chat_id: int,
    user_id: int,
    session: AsyncSession = Depends(get_session)
):
    # Accept the websocket connection
    await websocket.accept()

    # Add the websocket to the set of connected websockets
    connected_websockets.add(websocket)

    # Retrieve the chat and user objects from the database
    chat = await session.get(Chat, chat_id)
    user = await session.get(User, user_id)

    if chat is None or user is None:
        await websocket.close()
        return

    # Loop to receive and broadcast messages
    while True:
        try:
            message = await websocket.receive_text()
        except WebSocketDisconnect:
            # Remove the websocket from the set of connected websockets
            connected_websockets.remove(websocket)
            break

        now = datetime.utcnow()
        message_obj = Message(text=message, chat=chat,
                              user=user, created_at=now)
        session.add(message_obj)
        await session.commit()

        # Broadcast the message to all connected websockets in the chat
        for ws in connected_websockets:
            if ws != websocket:
                await ws.send_text(f'{user.name}: {message}')
