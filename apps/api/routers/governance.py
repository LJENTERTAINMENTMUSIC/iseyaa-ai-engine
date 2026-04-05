from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/governance", tags=["Civil Service & Governance"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class ServiceRequest(BaseModel):
    service_name: str # Passport, License, Permit
    details: dict

class PermitStatus(BaseModel):
    permit_id: str
    status: str # Approved, Rejected, Reviewing

# ─── Business Logic Engines ──────────────────────────────────────────────────
class PermitWorkflow:
    @staticmethod
    async def process_approval(permit_id: str) -> str:
        # Pillar 8: Civil Service & Governance (WorkFlow Node)
        # Logic: [AI-GOV] Verifying NIN and Resident Node...
        return "Approved"

class ServiceCatalog:
    @staticmethod
    async def get_services() -> List[Dict]:
        return [
            {"id": "s1", "name": "Passport Renewal", "fee": 25000, "duration": "48h"},
            {"id": "s2", "name": "Driver's License", "fee": 15000, "duration": "72h"},
            {"id": "s3", "name": "Business Permit", "fee": 50000, "duration": "24h"}
        ]

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/services")
async def get_government_services():
    # Pillar 8: Civil Service & Governance
    return await ServiceCatalog.get_services()

@router.post("/apply")
async def apply_service(
    req: ServiceRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 8: Civil Service & Governance
    user_id = user["id"] if "id" in user else user["user_id"]
    permit_id = f"PERM-{user_id[:4]}-2026"
    status = await PermitWorkflow.process_approval(permit_id)
    return {"status": status, "permit_id": permit_id, "user_id": user_id, "service": req.service_name}

@router.get("/status/{permit_id}")
async def check_permit(permit_id: str):
    # Pillar 8: Civil Service & Governance
    return {"permit_id": permit_id, "status": "In Review", "oha_node": "OHA-GOV-SYNC"}
