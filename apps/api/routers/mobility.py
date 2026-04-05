from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/mobility", tags=["Transport & Mobility"])

class BookingRequest(BaseModel):
    category: str # Flight, EBike, Car, Bus
    pickup: str
    dropoff: str
    fare: float
    metadata: Optional[Dict] = {}

@router.get("/vehicles")
async def get_vehicles(category: Optional[str] = Query(None)):
    # Pillar 2: Transport & Mobility
    conn = await db.get_db_conn()
    try:
        query = "SELECT * FROM vehicles WHERE status = 'active'"
        params = []
        if category:
            params.append(category)
            query += " AND category = $1"
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/book")
async def book_trip(
    req: BookingRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 2: Transport & Mobility (Full Cluster)
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO trips (user_id, pickup, dropoff, fare, category, metadata, status)
            VALUES ($1, $2, $3, $4, $5, $6, 'pending')
            RETURNING *
            """,
            user_id, req.pickup, req.dropoff, req.fare, req.category, req.metadata
        )
        return dict(row)
    finally:
        await conn.close()
