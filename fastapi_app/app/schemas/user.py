from __future__ import annotations

from pydantic import BaseModel, EmailStr


class UserOut(BaseModel):
    id: int
    email: EmailStr

    model_config = {"from_attributes": True}
