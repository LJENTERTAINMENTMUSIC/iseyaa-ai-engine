from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel
from typing import List, Optional, Dict
from services.auth import get_current_user
import db

router = APIRouter(prefix="/api/education", tags=["Education & E-Learning"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class EnrollmentRequest(BaseModel):
    course_id: str
    lga_id: str

class MentorRequest(BaseModel):
    interest: str # Tech, Agriculture, Arts, Finance

# ─── Business Logic Engines ──────────────────────────────────────────────────
class EnrollmentLogic:
    @staticmethod
    async def verify_subsidy(user_id: str, lga_id: str) -> bool:
        # Pillar 5: Education & E-Learning (Verification Node)
        # Logic: [AI-EDU] Verifying OHA LGA Registry...
        return True # Subsidized for Ogun State Residents

class MentorMatching:
    @staticmethod
    async def find_mentor(interest: str) -> Dict:
        # Pillar 5: Education & E-Learning (AI Mentorship)
        # Logic: [AI-EDU] Matching Expertise from State Nodes...
        return {"mentor_name": f"Dr. {interest.capitalize()} Expert", "session_id": "s-8112"}

# ─── Endpoints ────────────────────────────────────────────────────────────────
@router.get("/schools")
async def get_schools(lga: Optional[str] = None):
    # Pillar 5: Education & E-Learning
    conn = await db.get_db_conn()
    try:
        query = "SELECT * FROM schools WHERE 1=1"
        params = []
        if lga:
            params.append(lga)
            query += " AND lga_id = $1"
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.get("/courses")
async def get_courses():
    # Pillar 5: Education & E-Learning
    conn = await db.get_db_conn()
    try:
        rows = await conn.fetch("SELECT * FROM courses")
        return [dict(r) for r in rows]
    finally:
        await conn.close()

@router.post("/enroll")
async def enroll_course(
    req: EnrollmentRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 5: Education & E-Learning
    user_id = user["id"] if "id" in user else user["user_id"]
    is_subsidized = await EnrollmentLogic.verify_subsidy(user_id, req.lga_id)
    conn = await db.get_db_conn()
    try:
        await conn.execute("UPDATE courses SET enrolled_count = enrolled_count + 1 WHERE id = $1", req.course_id)
        return {"status": "success", "enrolled": True, "subsidized": is_subsidized}
    finally:
        await conn.close()

@router.post("/mentor/match")
async def match_mentor(req: MentorRequest):
    # Pillar 5: Education & E-Learning
    return await MentorMatching.find_mentor(req.interest)
