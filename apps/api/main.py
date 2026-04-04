"""
ISEYAA AI Engine — Backend API (FastAPI Edition)
Enterprise-grade engine for Ogun State Tourism & Governance
Aligned with PRD v1.1 Roadmap (Sprints 1-4)
"""

import os
import json
import datetime
import httpx
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# ─── Config ──────────────────────────────────────────────────────────────────
load_dotenv()
app = FastAPI(title="ISEYAA AI Engine", version="1.1.0")

# ─── Auth/DB Module ──────────────────────────────────────────────────────────
import db

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ─── CORS Middleware ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten in production (Squad Delta)
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Schemas (Pydantic) ───────────────────────────────────────────────────────
class ConciergeRequest(BaseModel):
    query: str
    context: Optional[dict] = None

class PlannerRequest(BaseModel):
    query: str
    destination_id: Optional[str] = None

class Destination(BaseModel):
    id: str
    title: str
    location: str
    category: str
    rating: float
    image: str
    description: str
    tags: List[str]
    opening_hours: Optional[str] = None
    entry_fee: Optional[str] = None
    lga: Optional[str] = None

class KycUpload(BaseModel):
    user_id: str
    document_type: str # 'nin', 'voters_card', 'passport'
    document_number: str
    file_url: str

class UserProfile(BaseModel):
    user_id: str
    full_name: str
    role: str
    kyc_status: str

# ─── Security Dependencies (Squad Alpha) ──────────────────────────────────────
async def get_current_user(request: Request) -> UserProfile:
    # Squad Alpha: Integration with Supabase JWT goes here
    # Mocking a verified government user for demo purposes if header present
    auth = request.headers.get("Authorization", "")
    if "govt-token" in auth:
        return UserProfile(user_id="123", full_name="Admin User", role="govt", kyc_status="verified")
    return UserProfile(user_id="456", full_name="Guest", role="traveler", kyc_status="unverified")

async def verify_govt_access(user: UserProfile = Body(..., embed=True)):
    if user.role != "govt" or user.kyc_status != "verified":
        raise HTTPException(status_code=403, detail="Access Denied: Government Verification Required (NIN/Passport)")
    return user

# ─── AI Concierge Mock Logic ──────────────────────────────────────────────────
SYSTEM_PROMPT = """You are Deep, ISEYAA's expert AI tourism concierge for Ogun State, Nigeria.
Speak in a warm, inspirational, slightly poetic tone — like a world-class tour guide."""

def smart_mock(query: str) -> str:
    q = query.lower()
    if "olumo" in q: return "Olumo Rock is Ogun State's crown jewel. Visiting at sunrise is magical."
    if "ojude" in q: return "The Ojude Oba Festival is Nigeria's most magnificent cultural spectacle."
    return f"Ogun State is full of wonders! For '{query}', I recommend starting at Olumo Rock."

# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {"status": "online", "platform": "ISEYAA AI Engine (FastAPI)", "version": "1.1.0"}

@app.get("/api/destinations")
async def get_destinations(category: str = "All", limit: int = 10):
    try:
        data = await db.fetch_destinations(limit=limit, category=category)
        return {"destinations": data, "total": len(data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/destinations/{id}")
async def get_destination(id: str):
    dest = await db.fetch_destination_by_id(id)
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    return dest

@app.get("/api/lga/{id}")
async def get_lga_profile(id: str):
    profile = await db.fetch_lga_profile(id)
    if not profile:
        raise HTTPException(status_code=404, detail="LGA intelligence profile not found")
    return profile

@app.get("/api/search")
async def search(q: str = ""):
    if not q: return {"results": [], "query": q, "total": 0}
    results = await db.search_destinations(q)
    return {"results": results, "query": q, "total": len(results)}

@app.post("/api/kyc/upload")
async def kyc_upload(req: KycUpload):
    # Module 7: Trust & Identity Service
    # (Squad Alpha: Save to kyc_documents table)
    print(f"[KYC] Received {req.document_type} for user {req.user_id}")
    return {
        "status": "pending",
        "message": f"Your {req.document_type} has been submitted for verification. Please allow 24-48 hours for review.",
        "tracking_id": "kyc_mock_5829"
    }

@app.get("/api/admin/stats")
async def admin_stats(request: Request):
    # Restricted Government Access
    user = await get_current_user(request)
    if user.role != "govt" or user.kyc_status != "verified":
        raise HTTPException(status_code=403, detail="KYC Verification Required: Access restricted to verified government officials only.")
    
    return {
        "revenue_total": "₦450.2M",
        "visitor_growth": "+12.5%",
        "active_hosts": 1420,
        "verified_lgas": 3
    }

@app.post("/api/ai/concierge")
async def concierge(req: ConciergeRequest):
    if not OPENAI_API_KEY:
        return {"status": "success", "response": smart_mock(req.query), "mode": "demo"}
    # (Squad Alpha: OpenAI integration stays here)
    return {"status": "success", "response": smart_mock(req.query), "mode": "demo"}

@app.post("/api/ai/planner")
async def planner(req: PlannerRequest):
    # Module 2 Agent v2
    itinerary = [
        {"day": 1, "activities": [
            {"time": "09:00 AM", "task": "Arrive at destination & Check-in", "tip": "Wear comfortable shoes."},
            {"time": "11:30 AM", "task": "Guided Historical Trek", "tip": "Ask about the ancestral stories."},
            {"time": "02:00 PM", "task": "Local Cuisine Lunch", "tip": "Try the regional specialty."}
        ]},
        {"day": 2, "activities": [
            {"time": "08:30 AM", "task": "Sunrise Photography Session", "tip": "Best light is before 9am."},
            {"time": "12:00 PM", "task": "Artisan Workshop / Market Visit", "tip": "Support local craftsmen."}
        ]}
    ]
    return {
        "status": "success",
        "destination_id": req.destination_id,
        "itinerary": itinerary,
        "note": "Personalized plan generated by Deep v2."
    }

@app.get("/api/weather")
async def weather():
    m = datetime.datetime.now().month
    rainy = 5 <= m <= 10
    return {
        "location": "Abeokuta, Ogun State",
        "temperature": 27 if rainy else 32,
        "condition": "Tropical showers" if rainy else "Sunny",
        "best_time_to_visit": "November – April"
    }

@app.get("/api/stats")
async def stats():
    return {
        "cultural_sites": 500, "annual_visitors": "3M+",
        "festivals_per_year": 120, "forest_area_km2": 4000
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
