from __future__ import annotations

import sys
import os
from pathlib import Path

import anyio
import httpx
from asgi_lifespan import LifespanManager

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.config import reset_settings_cache


def main() -> None:
    tmp = Path("._tmp_test")
    tmp.mkdir(exist_ok=True)

    os.environ["JWT_SECRET"] = "test-secret"
    os.environ["AUTO_CREATE_TABLES"] = "1"
    os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{(tmp / 'test.db').as_posix()}"
    reset_settings_cache()

    from app.main import create_app
    from app.core.security import hash_password

    try:
        hp = hash_password("Password123")
        print("hash_ok", hp[:20] + "...")
    except Exception as exc:  # noqa: BLE001
        print("hash_error", repr(exc))

    app = create_app()

    async def run() -> None:
        async with LifespanManager(app):
            transport = httpx.ASGITransport(app=app)
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                r = await client.post(
                    "/auth/register",
                    json={"email": "u1@example.com", "password": "Password123"},
                )
                print("status", r.status_code)
                print("body", r.text)

    anyio.run(run)


if __name__ == "__main__":
    main()
