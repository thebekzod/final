from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MessageCreate(BaseModel):
    receiver_id: int
    content: str


class MessageOut(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
