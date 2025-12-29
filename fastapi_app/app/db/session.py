from __future__ import annotations

from typing import AsyncGenerator

import structlog
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from app.core.config import get_settings

log = structlog.get_logger(__name__)

_engine: AsyncEngine | None = None
_sessionmaker: async_sessionmaker[AsyncSession] | None = None
_engine_url: str | None = None


def get_engine() -> AsyncEngine | None:
    return _engine


async def init_db_engine() -> None:
    global _engine, _sessionmaker, _engine_url
    url = get_settings().database_url
    if _engine is not None and _engine_url == url:
        return
    if _engine is not None and _engine_url != url:
        await _engine.dispose()
        _engine = None
        _sessionmaker = None
        _engine_url = None

    engine_kwargs = {"pool_pre_ping": True}
    if url.startswith("sqlite"):
        engine_kwargs["poolclass"] = NullPool
    _engine = create_async_engine(url, **engine_kwargs)
    _sessionmaker = async_sessionmaker(_engine, expire_on_commit=False)
    _engine_url = url
    log.info("db_engine_initialized")


async def close_db_engine() -> None:
    global _engine, _sessionmaker, _engine_url
    if _engine is None:
        return
    await _engine.dispose()
    _engine = None
    _sessionmaker = None
    _engine_url = None
    log.info("db_engine_closed")


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if _sessionmaker is None:
        raise RuntimeError("Database engine not initialized")
    async with _sessionmaker() as session:
        yield session
