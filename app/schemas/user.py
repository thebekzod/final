from __future__ import annotations

from datetime import datetime

from typing import Literal

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    role: Literal["freelancer", "employer"]


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["freelancer", "employer"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
