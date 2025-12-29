from __future__ import annotations

from pydantic import BaseModel


class CreditsBalanceOut(BaseModel):
    plan: str
    monthly_allowance: int
    remaining: int
    resets_at_iso: str


class CreditUsageItemOut(BaseModel):
    id: str
    at_iso: str
    action: str
    cost: int
