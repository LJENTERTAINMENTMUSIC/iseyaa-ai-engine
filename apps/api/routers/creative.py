from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/creative", tags=["Arts, Culture & Creative Economy"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class AssetRequest(BaseModel):
    title: str
    category: str # DigitalArt, Music, NFT, Heritage
    price: float

# ─── Business Logic Engines ──────────────────────────────────────────────────
class AssetGallery:
    @staticmethod
    async def get_assets() -> List[Dict]:
        return [
            {"id": "a1", "title": "Olumo Rock Digital Twin", "category": "Heritage", "price": 150000},
            {"id": "a2", "title": "Ojude Oba 2026 Soundtrack", "category": "Music", "price": 5000},
            {"id": "a3", "title": "Egba Textile Pattern #01", "category": "DigitalArt", "price": 25000}
        ]

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/assets")
async def get_creative_assets():
    # Pillar 12: Arts, Culture & Creative Economy
    return await AssetGallery.get_assets()

@router.post("/assets/mint")
async def mint_asset(
    req: AssetRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 12: Arts, Culture & Creative Economy (Monetization Node)
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO creative_assets (title, category, creator_id, price)
            VALUES ($1, $2, $3, $4)
            RETURNING *
            """,
            req.title, req.category, user_id, req.price
        )
        return dict(row)
    finally:
        await conn.close()
