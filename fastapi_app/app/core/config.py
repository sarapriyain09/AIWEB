from __future__ import annotations

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Tasks API"
    database_url: str

    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    log_level: str = "INFO"

    # Dev/test convenience. In production, prefer migrations.
    auto_create_tables: bool = True

    # Comma-separated list of allowed origins for browsers.
    # Keep this restrictive by default.
    cors_origins: str = Field(default="http://127.0.0.1:5173,http://localhost:5173")

    # Regex alternative for local dev where the frontend port may vary.
    # Starlette's CORSMiddleware will accept an Origin if it matches this regex.
    cors_allow_origin_regex: str = Field(default=r"^http://(127\\.0\\.0\\.1|localhost)(:\\d+)?$")


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]


def reset_settings_cache() -> None:
    get_settings.cache_clear()
