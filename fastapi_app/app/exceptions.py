from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


def install_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ValueError)
    async def value_error_handler(_: Request, exc: ValueError) -> JSONResponse:
        msg = str(exc)
        if msg in {"invalid_credentials"}:
            return JSONResponse(status_code=401, content={"detail": "Invalid email or password"})
        if msg in {"email_already_registered"}:
            return JSONResponse(status_code=409, content={"detail": "Email already registered"})
        if msg in {"Invalid token"}:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        return JSONResponse(status_code=400, content={"detail": "Bad request"})

    @app.exception_handler(LookupError)
    async def lookup_error_handler(_: Request, exc: LookupError) -> JSONResponse:
        if str(exc) == "task_not_found":
            return JSONResponse(status_code=404, content={"detail": "Task not found"})
        return JSONResponse(status_code=404, content={"detail": "Not found"})
