from __future__ import annotations

from typing import Iterable

from app.models import FreelancerProfile, Job


def keyword_match(job: Job, profiles: Iterable[FreelancerProfile]) -> list[int]:
    job_text = f"{job.title} {job.description}".lower()
    matches: list[int] = []
    for profile in profiles:
        if any(keyword.strip() in job_text for keyword in profile.skills.lower().split(",")):
            matches.append(profile.user_id)
    return matches
