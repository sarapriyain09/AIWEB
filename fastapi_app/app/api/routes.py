from __future__ import annotations

from fastapi import APIRouter

from app.api.routers import auth, credits, health, tasks

api_router = APIRouter()

api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(credits.router, prefix="/credits", tags=["credits"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
