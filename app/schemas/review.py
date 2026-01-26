from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class ReviewCreate(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    comment: str


class ReviewOut(ReviewCreate):
    id: int
    employer_id: int
    freelancer_id: int
    created_at: datetime

    class Config:
        from_attributes = True
