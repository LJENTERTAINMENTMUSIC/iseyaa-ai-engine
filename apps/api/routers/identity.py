from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/identity", tags=["Identity & Security"])

class KycRequest(BaseModel):
    doc_type: str
    doc_num: str
    file_url: str

@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"user": user}

@router.post("/kyc/submit")
async def submit_kyc(
    req: KycRequest,
    user: dict = Depends(get_current_user)
):
    # This is Pillar 13: Security & Identity
    result = await db.submit_kyc(user["id"] if "id" in user else user["user_id"], req.doc_type, req.doc_num, req.file_url)
    return result

@router.get("/kyc/status")
async def get_kyc_status(user: dict = Depends(get_current_user)):
    status = await db.get_kyc_status(user["id"] if "id" in user else user["user_id"])
    return {"status": status}
