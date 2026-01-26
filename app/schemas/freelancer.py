from __future__ import annotations

from pydantic import BaseModel

from app.schemas.user import UserOut


class FreelancerProfileCreate(BaseModel):
    skills: str
    experience_years: int
    hourly_rate: int
    bio: str


class FreelancerProfileOut(FreelancerProfileCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class FreelancerOut(BaseModel):
    user: UserOut
    profile: FreelancerProfileOut
