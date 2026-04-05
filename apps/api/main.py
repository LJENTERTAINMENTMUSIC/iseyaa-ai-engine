from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# ISEYAA "Launch 2.0" Routers
from routers import identity, hospitality, commerce, finance

load_dotenv()

app = FastAPI(title="ISEYAA AI State Operating System", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class AIRequest(BaseModel):
    query: str
    context: dict = None

# ─── Register Pillar Routers ──────────────────────────────────────────────────
app.include_router(identity.router)
app.include_router(hospitality.router)
app.include_router(commerce.router)
app.include_router(finance.router)

# ─── Pillar 10: AI Automation & Agent Layer (Orchestrator) ────────────────────
@app.post("/api/ai/concierge")
async def concierge(req: AIRequest):
    query = req.query.lower()
    
    if "book" in query or "stay" in query:
        return {"response": "I can help with that. I'm opening the Hospitality node for you."}
    if "buy" in query or "market" in query:
        return {"response": "Exploring the Digital Marketplace? I can show you local crafts."}
    if "pay" in query or "bill" in query:
        return {"response": "I'm redirecting you to the Utilities hub."}
        
    return {"response": "I am Deep, your Ogun State AI Guide. How can I assist you with our State Operating System today?"}

# ─── Pillar 12: Showcase Node ────────────────────────────────────────────────
@app.get("/api/showcase/billboards")
async def get_billboards():
    return [
        {"id": "b1", "image": "https://images.unsplash.com/photo-1590059397621-1f9502816997?auto=format&fit=crop&q=80&w=1200", "title": "Discover Ogun", "link": "/#explore"},
        {"id": "b2", "image": "https://images.unsplash.com/photo-1541462608141-ad7c68832a83?auto=format&fit=crop&q=80&w=1200", "title": "Ojude Oba 2026", "link": "/#events"}
    ]

@app.get("/api/showcase/featured")
async def get_featured():
    return {
        "events": [{"id": "e1", "title": "Ogun Arts Expo", "date": "June 2026"}],
        "vendors": [{"id": "v1", "name": "Egba Textile hub", "specialty": "Adire"}]
    }

# ─── Webhook ─────────────────────────────────────────────────────────────────
@app.post("/api/payments/webhook")
async def paystack_webhook(request: Request):
    try:
        body = await request.json()
        return {"status": "received", "event": body.get("event")}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"ISEYAA AI Launch 2.0 (Stable) starting on http://0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
