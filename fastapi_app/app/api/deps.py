from __future__ import annotations

from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.db.session import get_db
from app.repositories.user_repo import UserRepository

bearer_scheme = HTTPBearer(auto_error=False)


async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db():
        yield session


async def get_current_user_id(
    creds: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> int:
    if creds is None or not creds.credentials:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        subject = decode_token(creds.credentials)
        return int(subject)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    db: AsyncSession = Depends(db_session),
    user_id: int = Depends(get_current_user_id),
):
    repo = UserRepository()
    user = await repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
