from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    freelancer_profile: Mapped["FreelancerProfile"] = relationship(
        "FreelancerProfile", back_populates="user", uselist=False
    )


class FreelancerProfile(Base):
    __tablename__ = "freelancer_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False
    )
    skills: Mapped[str] = mapped_column(String(500), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False)
    hourly_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    bio: Mapped[str] = mapped_column(String(1000), nullable=False)

    user: Mapped[User] = relationship("User", back_populates="freelancer_profile")
