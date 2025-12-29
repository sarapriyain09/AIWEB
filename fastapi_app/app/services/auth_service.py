from __future__ import annotations

from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repo import UserRepository


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    async def register(self, db, *, email: str, password: str):
        existing = await self._users.get_by_email(db, email)
        if existing:
            raise ValueError("email_already_registered")
        user = await self._users.create(db, email=email, hashed_password=hash_password(password))
        token = create_access_token(str(user.id))
        return user, token

    async def login(self, db, *, email: str, password: str) -> str:
        user = await self._users.get_by_email(db, email)
        if not user:
            raise ValueError("invalid_credentials")
        if not verify_password(password, user.hashed_password):
            raise ValueError("invalid_credentials")
        return create_access_token(str(user.id))
