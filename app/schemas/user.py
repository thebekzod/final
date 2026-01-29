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
    password_confirm: str
    first_name: str
    last_name: str
    phone: str
    role: Literal["freelancer", "employer"]


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime
    first_name: str
    last_name: str
    phone: str

    class Config:
        from_attributes = True
