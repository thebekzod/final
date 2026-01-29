# NEONHIRE

NEONHIRE is a bilingual (EN/RU) two-sided freelance marketplace built with FastAPI + SQLite and a futuristic glassmorphism UI. It is designed as a clean diploma/portfolio project that runs on Python 3.13 (Windows) with pure-Python dependencies.

## Features
- JWT authentication with SHA-256 + salt password hashing.
- Freelancer onboarding and employer job posting.
- Freelancer directory with likes and reviews.
- Job board with employer controls.
- Real-time chat via WebSocket.
- Client-side EN/RU language toggle on every page.

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy 2.0 async, SQLite (aiosqlite)
- **Frontend:** Multi-page HTML, Tailwind CDN, vanilla JS
- **Auth:** python-jose JWT + hashlib

## Project Structure
```
app/
  main.py
  config.py
  database.py
  dependencies.py
  models/
  schemas/
  routers/
  services/
  utils/
  static/
  templates/
```

## Setup (Python 3.13)
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create `.env` from the example:
   ```bash
   copy .env.example .env
   ```
4. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```
5. Open the app:
   - http://127.0.0.1:8000/

## Demo Scenario (Examiner)
1. Register as **Employer**.
2. Create your first job post during onboarding.
3. Register as **Freelancer** in another browser or incognito.
4. Fill in the freelancer profile.
5. Employer opens **Freelancers** and leaves a like/review.
6. Freelancer opens **Jobs** and browses opportunities.
7. Open **Chat** and send a message between user IDs.

## API Overview
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/freelancers/profile`
- `GET /api/freelancers`
- `GET /api/freelancers/{id}`
- `POST /api/freelancers/{id}/like`
- `GET /api/freelancers/{id}/reviews`
- `POST /api/freelancers/{id}/reviews`
- `POST /api/jobs`
- `GET /api/jobs`
- `GET /api/jobs/{id}`
- `DELETE /api/jobs/{id}`
- `GET /api/chat/history/{user_id}`
- `WS /api/chat/ws?token=JWT`

## Notes
- SQLite database file `neonhire.db` is created automatically.
- Client-side language toggle is stored in localStorage.
