from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user
from app.schemas.auth import AuthResponse
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import authenticate_user, register_user
from app.utils.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    user = await register_user(session, payload)
    token = create_access_token(str(user.id))
    return AuthResponse(token=TokenResponse(access_token=token), user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    user = await authenticate_user(session, payload.email, payload.password)
    token = create_access_token(str(user.id))
    return AuthResponse(token=TokenResponse(access_token=token), user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)
