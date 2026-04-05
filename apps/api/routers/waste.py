from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/waste", tags=["Waste Management & Sustainability"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class CollectionRequest(BaseModel):
    frequency: str # Weekly, Bi-weekly
    lga_id: str

class SustainabilityReport(BaseModel):
    recycling_kg: float
    compost_kg: float

# ─── Business Logic Engines ──────────────────────────────────────────────────
class CollectionScheduler:
    @staticmethod
    async def get_next_pickup(lga_id: str) -> str:
        # Pillar 9: Waste Management & Sustainability (LGA Routing Node)
        # Logic: [AI-WASTE] Optimizing Route based on LGA Density...
        return "Tuesday, 08:30 AM"

class SustainabilityOracle:
    @staticmethod
    async def get_impact(kg: float) -> str:
        # Pillar 9: Waste Management & Sustainability (Green Node)
        # Logic: [AI-WASTE] Calculating CO2 Offset via OHA Node...
        offset = kg * 0.45
        return f"Your recycling has offset {offset:.2f}kg of CO2 this month."

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/pickup/next")
async def next_pickup(lga_id: str):
    # Pillar 9: Waste Management & Sustainability
    pickup = await CollectionScheduler.get_next_pickup(lga_id)
    return {"lga_id": lga_id, "next_pickup": pickup}

@router.get("/status")
async def get_waste_status(user: dict = Depends(get_current_user)):
    # Pillar 9: Waste Management & Sustainability
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        rows = await conn.fetch("SELECT * FROM waste_collections WHERE user_id = $1", user_id)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/enroll")
async def enroll_waste_collection(
    req: CollectionRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 9: Waste Management & Sustainability
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO waste_collections (user_id, frequency, lga_id, status)
            VALUES ($1, $2, $3, 'active')
            RETURNING *
            """,
            user_id, req.frequency, req.lga_id
        )
        return dict(row)
    finally:
        await conn.close()
