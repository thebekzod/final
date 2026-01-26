from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"


def html_response(filename: str) -> FileResponse:
    return FileResponse(TEMPLATES_DIR / filename)


@router.get("/")
async def login_page() -> FileResponse:
    return html_response("login.html")


@router.get("/register")
async def register_page() -> FileResponse:
    return html_response("register.html")


@router.get("/onboarding/freelancer")
async def onboarding_freelancer() -> FileResponse:
    return html_response("onboarding_freelancer.html")


@router.get("/onboarding/employer")
async def onboarding_employer() -> FileResponse:
    return html_response("onboarding_employer.html")


@router.get("/app/freelancers")
async def app_freelancers() -> FileResponse:
    return html_response("app_freelancers.html")


@router.get("/app/jobs")
async def app_jobs() -> FileResponse:
    return html_response("app_jobs.html")


@router.get("/app/chat")
async def app_chat() -> FileResponse:
    return html_response("app_chat.html")
