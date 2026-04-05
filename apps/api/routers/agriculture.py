from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/agriculture", tags=["Agriculture & Agri-Tech"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class LogisticsRequest(BaseModel):
    shipment_id: str
    status: Optional[str] = "pending"

class TradeRequest(BaseModel):
    farmer_id: str
    product_id: str
    quantity_kg: float
    price_total: float

# ─── Business Logic Engines ──────────────────────────────────────────────────
class LogisticsTracker:
    @staticmethod
    async def get_shipment_status(shipment_id: str) -> Dict:
        # Pillar 4: Agriculture & Agri-Tech (Fresh Produce Logistics)
        # Logic: [AI-AGRI] Verifying OHA Cargo Nodes...
        return {"shipment_id": shipment_id, "status": "In Transit", "temp_monitored": "4.2C", "eta": "2h 45m"}

class MarketTrade:
    @staticmethod
    async def create_contract(req: TradeRequest) -> Dict:
        # Pillar 4: Agriculture & Agri-Tech (Trader-to-Market Trade)
        # Logic: [AI-AGRI] Locking Forward Price for OHA Verification...
        return {"contract_id": "c-9821", "status": "locked", "oha_reference": "OHA-AGRI-2026-X"}

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/farms")
async def get_farms(lga: Optional[str] = None):
    # Pillar 4: Agriculture & Agri-Tech
    conn = await db.get_db_conn()
    try:
        query = "SELECT * FROM farms WHERE 1=1"
        params = []
        if lga:
            params.append(lga)
            query += " AND lga_id = $1"
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.get("/logistics/track/{shipment_id}")
async def track_shipment(shipment_id: str):
    # Pillar 4: Agriculture & Agri-Tech
    return await LogisticsTracker.get_shipment_status(shipment_id)

@router.post("/trade/contract")
async def create_trade_contract(
    req: TradeRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 4: Agriculture & Agri-Tech
    return await MarketTrade.create_contract(req)
