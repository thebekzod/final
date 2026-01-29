from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from uuid import uuid4

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.database import Base, SessionLocal, engine
from app.schemas.user import UserCreate
from app.services.auth_service import authenticate_user, register_user


async def main() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    email = f"smoke_{uuid4().hex}@example.com"
    payload = UserCreate(
        email=email,
        password="SmokeTest123!",
        password_confirm="SmokeTest123!",
        first_name="Smoke",
        last_name="Tester",
        phone="+10000000000",
        role="freelancer",
    )

    async with SessionLocal() as session:
        user = await register_user(session, payload)
        assert user.id, "Expected registered user to have an id"

    async with SessionLocal() as session:
        authenticated = await authenticate_user(session, email, payload.password)
        assert authenticated.id == user.id, "Expected login to return the created user"

    print(f"Smoke auth success for {email}")


if __name__ == "__main__":
    asyncio.run(main())
