from fastapi import APIRouter, Depends, HTTPException, Body, Query
from pydantic import BaseModel
from typing import List, Optional
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/commerce", tags=["Digital Marketplace & Food Vendors"])

class OrderRequest(BaseModel):
    merchant_id: str
    items: List[dict]
    total: float

@router.get("/merchants")
async def get_merchants(category: Optional[str] = Query(None)):
    # Pillar 1: Digital Marketplace
    return await db.get_merchants(category=category)

@router.get("/products")
async def get_products(merchant_id: Optional[str] = Query(None)):
    # Pillar 1: Digital Marketplace
    return await db.get_products(merchant_id=merchant_id)

@router.post("/orders/create")
async def create_order(
    req: OrderRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 1: Digital Marketplace
    # 1. Create order in DB
    user_id = user["id"] if "id" in user else user["user_id"]
    order = await db.create_order(user_id, req.merchant_id, req.items, req.total)
    
    # 2. Record Commission (OHA Governance Node)
    commission = float(req.total) * 0.05
    await db.record_commission(order["id"], commission)
    
    return {"order": order, "commission": commission}
