from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    title: str
    description: str
    budget: int


class JobOut(JobCreate):
    id: int
    employer_id: int
    created_at: datetime

    class Config:
        from_attributes = True
