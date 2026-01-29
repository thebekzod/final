from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import FreelancerProfile, Like, Review, User
from app.schemas.freelancer import FreelancerOut, FreelancerProfileCreate, FreelancerProfileOut
from app.schemas.review import ReviewCreate, ReviewOut

router = APIRouter(prefix="/api/freelancers", tags=["freelancers"])


@router.post("/profile", response_model=FreelancerProfileOut)
async def create_profile(
    payload: FreelancerProfileCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("freelancer")),
) -> FreelancerProfileOut:
    existing = await session.execute(
        select(FreelancerProfile).where(FreelancerProfile.user_id == current_user.id)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile exists")

    profile = FreelancerProfile(user_id=current_user.id, **payload.model_dump())
    session.add(profile)
    await session.commit()
    await session.refresh(profile)
    return FreelancerProfileOut.model_validate(profile)


@router.get("", response_model=list[FreelancerOut])
async def list_freelancers(session: AsyncSession = Depends(get_session)) -> list[FreelancerOut]:
    result = await session.execute(select(User, FreelancerProfile).join(FreelancerProfile))
    freelancers: list[FreelancerOut] = []
    for user, profile in result.all():
        freelancers.append(FreelancerOut(user=user, profile=profile))
    return freelancers


@router.get("/{freelancer_id}", response_model=FreelancerOut)
async def get_freelancer(
    freelancer_id: int, session: AsyncSession = Depends(get_session)
) -> FreelancerOut:
    result = await session.execute(
        select(User, FreelancerProfile)
        .join(FreelancerProfile)
        .where(User.id == freelancer_id)
    )
    row = result.first()
    if not row:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Freelancer not found")
    user, profile = row
    return FreelancerOut(user=user, profile=profile)


@router.post("/{freelancer_id}/like")
async def like_freelancer(
    freelancer_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("employer")),
) -> dict[str, str]:
    if freelancer_id == current_user.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot like yourself")
    existing = await session.execute(
        select(Like).where(
            Like.employer_id == current_user.id, Like.freelancer_id == freelancer_id
        )
    )
    if existing.scalar_one_or_none():
        return {"status": "already_liked"}
    like = Like(employer_id=current_user.id, freelancer_id=freelancer_id)
    session.add(like)
    await session.commit()
    return {"status": "liked"}


@router.get("/{freelancer_id}/reviews", response_model=list[ReviewOut])
async def list_reviews(
    freelancer_id: int, session: AsyncSession = Depends(get_session)
) -> list[ReviewOut]:
    result = await session.execute(select(Review).where(Review.freelancer_id == freelancer_id))
    return [ReviewOut.model_validate(review) for review in result.scalars().all()]


@router.post("/{freelancer_id}/reviews", response_model=ReviewOut)
async def create_review(
    freelancer_id: int,
    payload: ReviewCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("employer")),
) -> ReviewOut:
    review = Review(
        employer_id=current_user.id,
        freelancer_id=freelancer_id,
        rating=payload.rating,
        comment=payload.comment,
    )
    session.add(review)
    await session.commit()
    await session.refresh(review)
    return ReviewOut.model_validate(review)
