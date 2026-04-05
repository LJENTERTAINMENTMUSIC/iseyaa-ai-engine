from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/health", tags=["Healthcare & Telemedicine"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class ConsultationRequest(BaseModel):
    clinic_id: str
    type: str # In-person, Telemedicine
    symptoms: Optional[str] = None

class TriageResult(BaseModel):
    priority: str # Emergency, Urgent, Routine
    recommended_action: str
    estimated_wait_minutes: int

# ─── Business Logic Engines ──────────────────────────────────────────────────
class TriageEngine:
    @staticmethod
    def evaluate(symptoms: str) -> TriageResult:
        symptoms = symptoms.lower() if symptoms else ""
        if any(w in symptoms for w in ["heart", "breath", "unconscious", "chest"]):
            return TriageResult(priority="Emergency", recommended_action="Dispatching State Ambulance Node immediately.", estimated_wait_minutes=0)
        if any(w in symptoms for w in ["fever", "pain", "broken", "fracture"]):
            return TriageResult(priority="Urgent", recommended_action="Please proceed to the nearest Primary Health Center (PHC).", estimated_wait_minutes=15)
        return TriageResult(priority="Routine", recommended_action="Scheduling a Telemedicine consultation with a GP.", estimated_wait_minutes=45)

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.post("/triage")
async def perform_triage(req: ConsultationRequest):
    # Pillar 3: Healthcare & Telemedicine (Triage Node)
    return TriageEngine.evaluate(req.symptoms)

@router.get("/clinics")
async def get_clinics(lga: Optional[str] = None):
    # Pillar 3: Healthcare & Telemedicine (Clinic Management)
    conn = await db.get_db_conn()
    try:
        query = "SELECT * FROM clinics WHERE 1=1"
        params = []
        if lga:
            params.append(lga)
            query += " AND lga_id = $1"
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/consultations/book")
async def book_consultation(
    req: ConsultationRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 3: Healthcare & Telemedicine (Clinician Matching)
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO consultations (user_id, clinic_id, type, status)
            VALUES ($1, $2, $3, 'pending')
            RETURNING *
            """,
            user_id, req.clinic_id, req.type
        )
        return dict(row)
    finally:
        await conn.close()
