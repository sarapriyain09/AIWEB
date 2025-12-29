from __future__ import annotations

import sys
from pathlib import Path
import os
import uuid

import pytest
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient

# Ensure local imports work when running via venv entrypoints.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import reset_settings_cache  # noqa: E402


def _init_test_env() -> None:
    os.environ.setdefault("JWT_SECRET", "test-secret")
    os.environ.setdefault("JWT_ALGORITHM", "HS256")
    os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    os.environ.setdefault("AUTO_CREATE_TABLES", "1")


_init_test_env()


@pytest.fixture
async def client(tmp_path):
    # Use SQLite so tests don't require Postgres running.
    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{db_path.as_posix()}"
    reset_settings_cache()

    from app.main import create_app  # local import after env setup

    app = create_app()
    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac


@pytest.fixture
def random_email() -> str:
    return f"u-{uuid.uuid4().hex}@example.com"
