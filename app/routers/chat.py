from __future__ import annotations

import json
from typing import Dict

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, status
from jose import JWTError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import SessionLocal, get_session
from app.dependencies import get_current_user
from app.models import Message, User
from app.schemas.message import MessageOut
from app.utils.security import decode_access_token

router = APIRouter(prefix="/api/chat", tags=["chat"])


class ConnectionManager:
    def __init__(self) -> None:
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int) -> None:
        self.active_connections.pop(user_id, None)

    async def send_personal_message(self, user_id: int, message: dict) -> None:
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json(message)


manager = ConnectionManager()


@router.get("/history/{user_id}", response_model=list[MessageOut])
async def chat_history(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> list[MessageOut]:
    result = await session.execute(
        select(Message).where(
            (Message.sender_id == current_user.id) & (Message.receiver_id == user_id)
            | ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
        )
    )
    return [MessageOut.model_validate(message) for message in result.scalars().all()]


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str | None = None) -> None:
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError, TypeError):
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    await manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message_payload = json.loads(data)
            receiver_id = int(message_payload.get("receiver_id"))
            content = str(message_payload.get("content", "")).strip()
            if not content:
                await websocket.send_json({"error": "Empty message"})
                continue
            async with SessionLocal() as session:
                new_message = Message(sender_id=user_id, receiver_id=receiver_id, content=content)
                session.add(new_message)
                await session.commit()
                await session.refresh(new_message)
                payload = MessageOut.model_validate(new_message).model_dump()
            await manager.send_personal_message(receiver_id, payload)
            await websocket.send_json(payload)
    except WebSocketDisconnect:
        manager.disconnect(user_id)
    except (json.JSONDecodeError, ValueError):
        manager.disconnect(user_id)
        await websocket.close(code=status.WS_1003_UNSUPPORTED_DATA)
