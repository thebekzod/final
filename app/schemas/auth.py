from __future__ import annotations

from pydantic import BaseModel

from app.schemas.token import TokenResponse
from app.schemas.user import UserOut


class AuthResponse(BaseModel):
    token: TokenResponse
    user: UserOut
