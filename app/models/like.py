from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (UniqueConstraint("employer_id", "freelancer_id", name="uq_like"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    freelancer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
