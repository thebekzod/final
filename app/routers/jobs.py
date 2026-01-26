from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.dependencies import get_current_user, require_role
from app.models import Job, User
from app.schemas.job import JobCreate, JobOut

router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@router.post("", response_model=JobOut)
async def create_job(
    payload: JobCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("employer")),
) -> JobOut:
    job = Job(employer_id=current_user.id, **payload.model_dump())
    session.add(job)
    await session.commit()
    await session.refresh(job)
    return JobOut.model_validate(job)


@router.get("", response_model=list[JobOut])
async def list_jobs(session: AsyncSession = Depends(get_session)) -> list[JobOut]:
    result = await session.execute(select(Job))
    return [JobOut.model_validate(job) for job in result.scalars().all()]


@router.get("/{job_id}", response_model=JobOut)
async def get_job(job_id: int, session: AsyncSession = Depends(get_session)) -> JobOut:
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return JobOut.model_validate(job)


@router.delete("/{job_id}")
async def delete_job(
    job_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(require_role("employer")),
) -> dict[str, str]:
    result = await session.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.employer_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")
    await session.delete(job)
    await session.commit()
    return {"status": "deleted"}
