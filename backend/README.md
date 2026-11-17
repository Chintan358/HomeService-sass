# Backend – Home Services Booking

This folder contains the FastAPI backend for the Home Services Booking SaaS.

## Running locally
```powershell
cd backend
poetry install  # install dependencies
copy .env.example .env  # edit as needed
poetry run uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Key packages
- **FastAPI** – REST API framework
- **SQLAlchemy** – ORM (MySQL in production, SQLite for dev)
- **Passlib** – password hashing (`bcrypt`)
- **PyJWT** – JWT handling
- **Pydantic** – request/response validation

## Project structure
```
backend/
├─ app/               # FastAPI app entry point
├─ core/              # config, security, DB session
├─ models/            # SQLAlchemy models
├─ routers/           # API routers (auth, users, services…)
├─ schemas/           # Pydantic schemas
├─ utils/             # shared utilities (dependencies, helpers)
├─ tests/             # pytest suite
└─ pyproject.toml     # Poetry dependencies
```

## Running tests
```powershell
poetry run pytest
```

The test suite creates an SQLite database (`test.db`) in the project root and tears it down after each run.
