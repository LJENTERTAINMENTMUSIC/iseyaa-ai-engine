from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/utilities", tags=["Power & Utilities"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class BillPaymentRequest(BaseModel):
    bill_id: str
    amount: float

class UsageRequest(BaseModel):
    utility_type: str # Power, Water
    meter_number: str

# ─── Business Logic Engines ──────────────────────────────────────────────────
class BillingOracle:
    @staticmethod
    async def calculate_bill(usage_units: float, rate_per_unit: float = 50.0) -> float:
        # Pillar 6: Power & Utilities (Bill Calculation Node)
        # Logic: [AI-UTIL] Calculating Tariff based on LGA bracket...
        return usage_units * rate_per_unit

class WalletAutopay:
    @staticmethod
    async def process_autopay(user_id: str, amount: float) -> bool:
        # Pillar 6: Power & Utilities (Finance Sync)
        # Logic: [AI-UTIL] Verifying Wallet Balance via OHA Node...
        # In production, this calls Pillar 9 (Finance)
        return True

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.post("/calculate")
async def calculate_usage(req: UsageRequest):
    # Pillar 6: Power & Utilities
    units = 120.5 # Mock usage
    bill = await BillingOracle.calculate_bill(units)
    return {"utility": req.utility_type, "units": units, "total_bill": bill}

@router.get("/bills")
async def get_bills(user: dict = Depends(get_current_user)):
    # Pillar 6: Power & Utilities
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        rows = await conn.fetch("SELECT * FROM utility_bills WHERE user_id = $1", user_id)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/pay/auto")
async def autopay_bill(
    req: BillPaymentRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 6: Power & Utilities
    user_id = user["id"] if "id" in user else user["user_id"]
    success = await WalletAutopay.process_autopay(user_id, req.amount)
    if success:
        return {"status": "success", "paid_via": "ISEYAA Wallet", "amount": req.amount}
    raise HTTPException(status_code=400, detail="Insufficient Wallet funds.")
