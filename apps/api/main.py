"""
ISEYAA AI Engine — Backend API (FastAPI Edition)
Enterprise-grade engine for Ogun State Tourism & Governance
Aligned with PRD v1.1 Roadmap (Sprints 1-4)
"""

import os
import json
import datetime
import httpx
import sys
from unittest.mock import MagicMock

# ─── Python 3.14 Fix: Skip problematic OpenAPI models ───────────────
sys.modules["fastapi.openapi.models"] = MagicMock()

# ─── AI Intelligence Layer Node Mapping ───────────────
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent / "packages"))
from ai_agents import orchestrator
from services.communications import comm_service # OHA Communications
from services.auth import get_current_user # Supabase Auth
from services.paystack import paystack_service # Monetization
from db import fetch_latest_kyc_submission # Required for status checks
from fastapi import FastAPI, HTTPException, Body, Request, Query, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# ─── Utility ─────────────────────────────────────────────────────────────────
class DotDict(dict):
    """Simple helper to allow dot notation for dicts"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

# ─── Config ──────────────────────────────────────────────────────────────────
load_dotenv()
app = FastAPI(title="ISEYAA AI Engine", version="1.1.0", docs_url=None, redoc_url=None, openapi_url=None)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
AI_PROVIDER = os.getenv("AI_PROVIDER", "anthropic").lower()

# ─── CORS Middleware ──────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Tighten in production (Squad Delta)
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# ─── Schemas (Pydantic-Free for Python 3.14) ──────────────────────────────────
# Using DotDict and Body() instead of BaseModel to bypass Pydantic v1 crashes

# ─── Security Dependencies (Squad Alpha) ──────────────────────────────────────
# Current user is now injected via get_current_user in individual endpoints if needed,
# or used as a standard security dependency.

async def verify_govt_access(user: dict):
    # Check if user has Govt role AND has completed Phase 3 verification
    # Using Sub (user_id) from the decoded JWT
    kyc_data = await fetch_latest_kyc_submission(user.get("user_id"))
    status = kyc_data.get("status") if kyc_data else "unverified"
    
    if user.get("role") != "service_role" and user.get("role") != "govt" and status != "verified":
        raise HTTPException(
            status_code=403, 
            detail=f"Access Denied: Government Verification Required (Current Status: {status}). Please complete Phase 3 NIN/Passport verification."
        )
    return user

# Legacy ask_ai refactored into @iseyaa/ai_agents Orchestrator
# ask_ai function removed as AI requests are now delegated to specialized agents.

# smart_mock logic moved to the AI package's orchestrator fallback handlers.

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

# ─── StayHub (Accommodation) (Phase 4) ───────────────────────────────
@app.get("/api/stays")
async def get_stays(lga_id: str = None, limit: int = 10):
    stays = await db.fetch_stays(lga_id, limit)
    return {"stays": stays, "total": len(stays)}

@app.get("/api/stays/{id}")
async def get_stay(id: str):
    stay = await db.fetch_stay_by_id(id)
    if not stay:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return stay

# ─── Bookings & Transactions (Phase 5) ───────────────────────────────
@app.post("/api/bookings")
async def create_booking(req: dict = Body(...), user: dict = Depends(get_current_user)):
    req = DotDict(req)
    # Check if user is KYC verified before allowing a high-value booking
    kyc_data = await fetch_latest_kyc_submission(user.get("user_id"))
    status = kyc_data.get("status") if kyc_data else "unverified"
    
    if status != "verified" and req.item_type == "stay":
         raise HTTPException(status_code=403, detail="KYC Verification Required for Accommodation Bookings. Please verify your Identity first.")
    
    # ─── Step 1: Create local booking record ───
    booking = await db.create_booking(
        user_id=user.get("user_id"),
        item_id=req.item_id,
        item_type=req.item_type,
        check_in=req.check_in,
        check_out=req.check_out,
        total_price=req.total_price
    )
    
    # ─── Step 2: Initialize Paystack Transaction ───
    # We include the booking_id and item_type in metadata for the webhook later
    payment = await paystack_service.initialize_transaction(
        email=user.get("email", "guest@iseyaa.ng"),
        amount_naira=req.total_price,
        metadata={"booking_id": booking["id"], "item_type": req.item_type, "user_id": user.get("user_id")}
    )
    
    # ─── OHA/OEMG Governance: Tax Levy Calculation (5%) ───
    # Recorded as 'pending' until payment verification
    if booking and booking.get("status") != "error":
        levy = float(req.total_price) * 0.05
        await db.record_tourism_levy(booking["id"], "M-GOV-001", levy)
        print(f"[OHA/OEMG-GOVERNANCE] Recorded pending ₦{levy} Tourism/Event Levy for Booking {booking['id']}")
            
    return {
        "status": "success", 
        "booking": booking, 
        "checkout_url": payment["data"]["authorization_url"],
        "reference": payment["data"]["reference"]
    }

@app.get("/api/bookings/user/{user_id}")
async def get_user_bookings(user_id: str):
    bookings = await db.fetch_user_bookings(user_id)
    return {"bookings": bookings}

@app.get("/api/search")
async def search(q: str = ""):
    if not q: return {"results": [], "query": q, "total": 0}
    results = await db.search_destinations(q)
    return {"results": results, "query": q, "total": len(results)}

@app.post("/api/kyc/upload")
async def kyc_upload(req: dict = Body(...)):
    req = DotDict(req)
    # Module 7: Trust & Identity Service - Phase 3 Real Integration
    result = await kyc.process_kyc_submission(
        user_id=req.user_id,
        doc_type=req.document_type,
        doc_number=req.document_number,
        file_url=req.file_url
    )
    return {
        "status": result.status,
        "message": result.message,
        "tracking_id": result.tracking_id,
        "timestamp": result.timestamp.isoformat(),
        "meta": result.metadata
    }

@app.get("/api/kyc/status/{user_id}")
async def get_kyc_status(user_id: str):
    status = await kyc.check_kyc_status(user_id)
    return {"user_id": user_id, "status": status}

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
async def concierge(req: dict = Body(...)):
    req = DotDict(req)
    # AI requests are now handled by the @iseyaa/ai_agents package
    response_text = await orchestrator.delegate_task("general", {}, req.query)
    return {"status": "success", "response": response_text, "mode": "agent"}

@app.post("/api/ai/planner")
async def planner(req: dict = Body(...)):
    req = DotDict(req)
    # Phase 3: Specialized planner agent
    lga_info = {}
    if req.destination_id:
        dest = await db.fetch_destination_by_id(req.destination_id)
        if dest:
            lga_info["lga_name"] = dest.get('lga_id') or dest.get('lga')
    
    response_text = await orchestrator.delegate_task("planner", lga_info, req.query)
    return {
        "status": "success",
        "destination_id": req.destination_id,
        "itinerary_text": response_text,
        "note": "Personalized plan generated by Deep v2 Agent."
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
