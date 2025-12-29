from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends

from app.api.deps import get_current_user_id
from app.schemas.credits import CreditUsageItemOut, CreditsBalanceOut

router = APIRouter()


@router.get("/balance", response_model=CreditsBalanceOut)
async def credits_balance(_: int = Depends(get_current_user_id)) -> CreditsBalanceOut:
    # Stub implementation: returns a fixed student plan.
    # Replace with real Stripe + ledger-backed credits logic.
    now = datetime.now(tz=UTC)
    resets_at = datetime(year=now.year + (1 if now.month == 12 else 0), month=(now.month % 12) + 1, day=1, tzinfo=UTC)

    return CreditsBalanceOut(
        plan="student",
        monthly_allowance=200,
        remaining=200,
        resets_at_iso=resets_at.isoformat(),
    )


@router.get("/usage", response_model=list[CreditUsageItemOut])
async def credits_usage(_: int = Depends(get_current_user_id)) -> list[CreditUsageItemOut]:
    # Stub implementation: empty list.
    return []
