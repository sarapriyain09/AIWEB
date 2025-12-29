from __future__ import annotations

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.init_db import create_all_tables
from app.db.session import close_db_engine, get_engine, init_db_engine
from app.exceptions import install_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    configure_logging(settings.log_level)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        await init_db_engine()
        s = get_settings()
        if s.auto_create_tables:
            engine = get_engine()
            if engine is not None:
                await create_all_tables(engine)
        try:
            yield
        finally:
            await close_db_engine()

    app = FastAPI(title=settings.app_name, lifespan=lifespan)

    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    origin_regex = settings.cors_allow_origin_regex.strip() if settings.cors_allow_origin_regex else ""
    if origins or origin_regex:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_origin_regex=origin_regex or None,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    install_exception_handlers(app)

    app.include_router(api_router)

    return app


app = create_app()
