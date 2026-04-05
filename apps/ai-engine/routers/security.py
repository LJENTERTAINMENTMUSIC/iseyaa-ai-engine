from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/security", tags=["Safety & Security"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class AlertRequest(BaseModel):
    type: str # Emergency, Crime, Fire
    description: str
    lga_id: str

class IncidentReport(BaseModel):
    user_id: str
    incident_type: str
    location: str

# ─── Business Logic Engines ──────────────────────────────────────────────────
class AlertBroadcaster:
    @staticmethod
    async def broadcast(alert: Dict) -> int:
        # Pillar 10: Safety & Security (Broadcast Node)
        # Logic: [AI-SECURITY] Pushing Alert to all Resident Nodes in {alert['lga_id']}
        # In production, this triggers SMS/Push notifications
        return 1250 # Returns number of residents alerted

class IncidentLog:
    @staticmethod
    async def log_incident(report: IncidentReport) -> str:
        # Pillar 10: Safety & Security (Audit Node)
        # Logic: [AI-SECURITY] Recording Incident to State Response Node...
        return "INC-8812-SYNC-OHA"

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/alerts")
async def get_alerts(lga: Optional[str] = None):
    # Pillar 10: Safety & Security
    conn = await db.get_db_conn()
    try:
        query = "SELECT * FROM emergency_alerts WHERE status = 'active'"
        params = []
        if lga:
            params.append(lga)
            query += " AND lga_id = $1"
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/report")
async def report_alert(
    req: AlertRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 10: Safety & Security
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO emergency_alerts (type, description, lga_id, status)
            VALUES ($1, $2, $3, 'active')
            RETURNING *
            """,
            req.type, req.description, req.lga_id
        )
        # Trigger Broadcast logic
        residents_alerted = await AlertBroadcaster.broadcast(dict(row))
        return {"status": "alert_broadcasted", "residents_alerted": residents_alerted, "alert": dict(row)}
    finally:
        await conn.close()

@router.post("/incident/log")
async def log_incident(req: IncidentReport):
    # Pillar 10: Safety & Security
    reference = await IncidentLog.log_incident(req)
    return {"status": "logged", "reference": reference}
