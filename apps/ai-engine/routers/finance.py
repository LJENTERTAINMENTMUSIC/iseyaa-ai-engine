from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from services.auth import get_current_user
from services.paystack import PaystackService
import db

router = APIRouter(prefix="/api/finance", tags=["Wallet & Infrastructure"])

class DepositRequest(BaseModel):
    amount: float

@router.get("/wallet/balance")
async def get_wallet_balance(user: dict = Depends(get_current_user)):
    # Pillar 9: User Wallet
    user_id = user["id"] if "id" in user else user["user_id"]
    balance = await db.get_user_balance(user_id)
    return {"balance": balance, "currency": "NGN"}

@router.post("/wallet/deposit")
async def wallet_deposit(
    req: DepositRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 9: User Wallet
    email = user["email"] if "email" in user else "traveler@iseyaa.ng"
    user_id = user["id"] if "id" in user else user["user_id"]
    
    paystack = PaystackService()
    ref = f"fund_{user_id}_{await db.get_timestamp()}"
    payment = await paystack.initialize_transaction(email, req.amount, ref)
    return {"payment": payment}

@router.get("/transactions")
async def get_transactions(user: dict = Depends(get_current_user)):
    # Pillar 9: User Wallet
    user_id = user["id"] if "id" in user else user["user_id"]
    return await db.get_user_transactions(user_id)
