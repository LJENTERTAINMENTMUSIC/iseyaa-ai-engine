from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Optional
from services.auth import get_current_user
from services.paystack import PaystackService
import db

router = APIRouter(prefix="/api/hospitality", tags=["Accommodation & Tourism"])

class BookingRequest(BaseModel):
    item_id: str
    item_type: str
    total_price: float

@router.get("/destinations")
async def get_destinations(
    category: Optional[str] = Query(None),
    lga: Optional[str] = Query(None)
):
    # Pillar 11: Tourism, Culture & Heritage
    return await db.get_destinations(category=category, lga=lga)

@router.get("/stays")
async def get_stays(
    lga: Optional[str] = Query(None),
    price_max: Optional[float] = Query(None)
):
    # Pillar 3: Accommodation & Hospitality
    return await db.get_stays(lga=lga, price_max=price_max)

@router.post("/bookings/create")
async def create_booking(
    req: BookingRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 3 & 11: Monetization via Paystack
    # 1. Create booking in DB
    user_id = user["id"] if "id" in user else user["user_id"]
    email = user["email"] if "email" in user else "traveler@iseyaa.ng"
    
    booking = await db.create_booking(user_id, req.item_id, req.item_type, req.total_price)
    
    # 2. Add 5% Tourism Levy (OHA Governance Node)
    levy = float(req.total_price) * 0.05
    await db.record_tax_levy(booking["id"], levy)
    
    # 3. Initialize Paystack Transaction
    paystack = PaystackService()
    payment = await paystack.initialize_transaction(email, req.total_price, booking["id"])
    
    return {"booking": booking, "payment": payment, "levy_recorded": levy}
