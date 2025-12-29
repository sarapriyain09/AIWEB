# FastAPI Clean Architecture (JWT + Tasks)

This is a production-ready starter backend using:
- FastAPI (REST)
- PostgreSQL
- SQLAlchemy (async)
- JWT auth (bearer)
- Pydantic validation
- Structured logging (JSON)
- Pytest (async)

## Run locally (without Docker)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Create a .env (see .env.example)
Copy-Item .env.example .env

uvicorn main:app --reload
```

## PowerShell helper
Common tasks (creates `.env` and venv for you):
```powershell
.\dev.ps1 init-env
.\dev.ps1 install
.\dev.ps1 run
.\dev.ps1 test
```

## Database migrations (Alembic)
This project supports Alembic migrations.

```powershell
# Create a migration
alembic revision --autogenerate -m "init"

# Apply migrations
alembic upgrade head
```

`--autogenerate` needs to connect to the database specified by `DATABASE_URL`.
If you don't have Postgres running locally, start the Docker DB:
```powershell
.\dev.ps1 docker-db
.\dev.ps1 migrate-init
.\dev.ps1 migrate-up
```

If you already have a local Postgres on `localhost:5432` with different credentials, update `.env` accordingly (or stop that service) so `DATABASE_URL` points to the correct instance.

If `alembic revision --autogenerate ...` fails, the usual causes are:
- dependencies not installed in your venv
- `.env` missing (so `DATABASE_URL` / `JWT_SECRET` are unset)

Using the helper:
```powershell
.\dev.ps1 init-env
.\dev.ps1 install
.\dev.ps1 migrate-init
.\dev.ps1 migrate-up
```

## Auto table creation
By default, tables are auto-created on startup for dev/test convenience.
Disable in production by setting `AUTO_CREATE_TABLES=0` and rely on Alembic migrations.

## Run with Docker
```powershell
docker compose up --build
```

API:
- `GET /health`
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `CRUD /tasks` (auth required)
