from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user
from app.schemas.auth import AuthResponse, RegisterResponse
from app.schemas.token import TokenResponse
from app.schemas.user import UserCreate, UserLogin, UserOut
from app.services.auth_service import authenticate_user, register_user
from app.utils.security import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])
logger = logging.getLogger(__name__)


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
async def register(
    payload: UserCreate, session: AsyncSession = Depends(get_session)
) -> RegisterResponse:
    try:
        await register_user(session, payload)
    except HTTPException as exc:
        logger.warning(
            "Registration failed status=%s detail=%s email=%s",
            exc.status_code,
            exc.detail,
            payload.email,
        )
        raise
    except Exception:
        logger.exception("Registration failed status=500 email=%s", payload.email)
        raise
    return RegisterResponse(message="Registration successful")


@router.post("/login", response_model=AuthResponse)
async def login(payload: UserLogin, session: AsyncSession = Depends(get_session)) -> AuthResponse:
    try:
        user = await authenticate_user(session, payload.email, payload.password)
    except HTTPException as exc:
        logger.warning(
            "Login failed status=%s detail=%s email=%s",
            exc.status_code,
            exc.detail,
            payload.email,
        )
        raise
    except Exception:
        logger.exception("Login failed status=500 email=%s", payload.email)
        raise
    token = create_access_token(str(user.id))
    return AuthResponse(token=TokenResponse(access_token=token), user=UserOut.model_validate(user))


@router.get("/me", response_model=UserOut)
async def me(current_user=Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(current_user)
