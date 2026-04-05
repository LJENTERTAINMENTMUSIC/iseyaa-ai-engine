import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# LGA Intelligence Profiles (Module 1 — Knowledge Graph)
LGA_PROFILES = {
    "abeokuta-south": {
        "name": "Abeokuta South",
        "region": "Egba",
        "origin_story": "Founded in 1830 by Sodeke after the Egba people escaped the Oyo Empire, using Olumo Rock as a natural fortress. This 'refuge under the rock' gave the city its name.",
        "notable_rulers": ["Alake of Egbaland (Oba Adedotun Aremu Gbadebo III)"],
        "economic_focus": ["Tourism", "Adire Textiles", "Civil Service"],
        "history_snip": "The heart of the Egba Confederacy and a historic node for Nigerian Christianity and education."
    },
    "ijebu-ode": {
        "name": "Ijebu Ode",
        "region": "Ijebu",
        "origin_story": "According to tradition, the town was founded by Obanta, an immigrant from Ile-Ife, who defeated the native rulers to establish the Ijebu Kingdom. It is a major node of trade between the coast and the hinterland.",
        "notable_rulers": ["Awujale of Ijebuland (Oba Sikiru Kayode Adetona)"],
        "economic_focus": ["Trade", "Agriculture", "Logistics"],
        "history_snip": "Home to the world-renowned Ojude Oba Festival, a symbol of religious harmony and cultural extravagance."
    },
    "sagamu": {
        "name": "Sagamu",
        "region": "Remo",
        "origin_story": "A confederation of 13 separate towns established in the 19th century to unite the Remo people against external threats. Its location makes it the 'Gateway' between Lagos and the rest of the country.",
        "notable_rulers": ["Akarigbo of Remoland (Oba Babatunde Adewale Ajayi)"],
        "economic_focus": ["Kolanut Trade", "Industrial Manufacturing", "Cement Production"],
        "history_snip": "The world's headquarters for Kolanut trade and a vital industrial hub for West Africa."
    }
}

# In‑memory fallback data (expanded with PRD v1.1 seed data)
_FALLBACK_DESTINATIONS = [
    {
        "id": "olumo-rock",
        "title": "Olumo Rock",
        "location": "Abeokuta, Ogun South",
        "lga": "abeokuta-south",
        "category": "Heritage",
        "rating": 4.9,
        "image": "/olumo-rock.png",
        "description": "A sacred granite monolith rising 137m from the tropical forest canopy, revered for over 500 years by the Egba people. Offers breathtaking panoramic views of Abeokuta city below.",
        "tags": ["historical", "heritage", "views", "hiking", "UNESCO"],
        "opening_hours": "8:00 AM – 6:00 PM daily",
        "entry_fee": "₦500 adults",
    },
    {
        "id": "ojude-oba-precinct",
        "title": "Awujale Palace (Ojude Oba)",
        "location": "Ijebu-Ode, Ogun State",
        "lga": "ijebu-ode",
        "category": "Heritage",
        "rating": 5.0,
        "image": "/festival.png",
        "description": "The ancestral seat of the Ijebu Kingdom. Every year, thousands gather here for the horse parades and cultural displays of the Ojude Oba festival.",
        "tags": ["palace", "culture", "monarch", "archaeology", "photography"],
        "opening_hours": "Contact Palace Office for tours",
        "entry_fee": "Free public access to exterior",
    },
    {
        "id": "sagamu-kola-market",
        "title": "Akarigbo Kolanut Hub",
        "location": "Sagamu, Remo Region",
        "lga": "sagamu",
        "category": "Experience",
        "rating": 4.6,
        "image": "/market.png",
        "description": "The historical heart of the world's kolanut trade. Witness the ancient grading and trading traditions that have powered the Remo economy for a century.",
        "tags": ["market", "economic", "agriculture", "trade-history"],
        "opening_hours": "7:00 AM – 4:00 PM (Best visiting time)",
        "entry_fee": "Free",
    },
    {
        "id": "ogun-forest-canopy",
        "title": "Ogun Forest Canopy Walk",
        "location": "Ogun Forest Reserve",
        "lga": "remains-unmapped",
        "category": "Nature",
        "rating": 4.8,
        "image": "/jungle-interior.png",
        "description": "Walk beneath a living cathedral of giant monstera leaves and ancient rainforest giants. God rays of sunlight pierce the canopy in a mystical display of natural light.",
        "tags": ["nature", "forest", "ecotourism", "photography", "wildlife"],
        "opening_hours": "7:00 AM – 5:00 PM",
        "entry_fee": "₦1,000",
    },
    {
        "id": "ogun-waterfall",
        "title": "Ogun Jungle Waterfall",
        "location": "Osun Forest Reserve",
        "lga": "remains-unmapped",
        "category": "Nature",
        "rating": 4.9,
        "image": "/waterfall.png",
        "description": "A multi‑tiered cascade plunging into emerald pools deep within the rainforest. Mist from the falls keeps the surrounding jungle impossibly lush.",
        "tags": ["waterfall", "swimming", "nature", "hiking", "photography"],
        "opening_hours": "8:00 AM – 4:00 PM",
        "entry_fee": "₦800",
    }
]

_pool = None

async def get_pool():
    global _pool
    if not DATABASE_URL:
        return None
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)
    return _pool

async def fetch_lga_profile(lga_id: str):
    pool = await get_pool()
    if not pool:
        return LGA_PROFILES.get(lga_id.lower())
    
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM lga_profiles WHERE id = $1", lga_id.lower())
        if row:
            import json
            data = dict(row)
            # Handle jsonb fields which asyncpg returns as dict/list automatically or as strings depending on config
            # But usually it returns them as dict/list.
            return data
    return LGA_PROFILES.get(lga_id.lower())

async def fetch_destinations(limit: int = 10, category: str = None):
    pool = await get_pool()
    if not pool:
        data = _FALLBACK_DESTINATIONS
        if category and category.lower() != "all":
            data = [d for d in data if d["category"].lower() == category.lower()]
        return data[:limit]

    async with pool.acquire() as conn:
        query = "SELECT * FROM destinations"
        params = []
        if category and category.lower() != "all":
            query += " WHERE category = $1"
            params.append(category)
        query += f" LIMIT ${len(params) + 1}"
        params.append(limit)
        
        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]

async def fetch_destination_by_id(dest_id: str):
    pool = await get_pool()
    if not pool:
        return next((d for d in _FALLBACK_DESTINATIONS if d["id"] == dest_id), None)

    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM destinations WHERE id = $1", dest_id)
        if row:
            return dict(row)
    return next((d for d in _FALLBACK_DESTINATIONS if d["id"] == dest_id), None)

async def search_destinations(query: str):
    pool = await get_pool()
    if not pool:
        q = query.lower()
        results = []
        for dest in _FALLBACK_DESTINATIONS:
            score = 0
            if q in dest["title"].lower(): score += 10
            if q in dest["location"].lower(): score += 5
            if score > 0:
                results.append({**dest, "_score": score})
        return sorted(results, key=lambda x: x["_score"], reverse=True)

    async with pool.acquire() as conn:
        # Simple ILIKE search for title and location
        rows = await conn.fetch(
            "SELECT *, 10 as _score FROM destinations WHERE title ILIKE $1 OR location ILIKE $1",
            f"%{query}%"
        )
        return [dict(row) for row in rows]

async def save_kyc_submission(user_id: str, doc_type: str, doc_number: str, file_url: str, tracking_id: str, status: str):
    pool = await get_pool()
    if not pool:
        print(f"[DB-FALLBACK] Saving KYC {tracking_id} to in-memory log bundle.")
        return True

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO kyc_submissions (user_id, document_type, document_number, file_url, tracking_id, status, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, NOW())
            ON CONFLICT (tracking_id) DO UPDATE SET status = $6, updated_at = NOW()
            """,
            user_id, doc_type, doc_number, file_url, tracking_id, status
        )
    return True

async def fetch_latest_kyc_submission(user_id: str):
    pool = await get_pool()
    if not pool:
        return {"status": "pending"} # Fallback for demo

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "SELECT * FROM kyc_submissions WHERE user_id = $1 ORDER BY created_at DESC LIMIT 1",
            user_id
        )
        if row:
            return dict(row)
    return None

# ─── StayHub (Accommodation) (Phase 4) ───────────────────────────────
async def fetch_stays(lga_id: str = None, limit: int = 10):
    pool = await get_pool()
    if not pool:
        # Fallback for demo
        return []

    async with pool.acquire() as conn:
        if lga_id:
            rows = await conn.fetch("SELECT * FROM stays WHERE lga_id = $1 LIMIT $2", lga_id, limit)
        else:
            rows = await conn.fetch("SELECT * FROM stays LIMIT $1", limit)
        return [dict(row) for row in rows]

async def fetch_stay_by_id(stay_id: str):
    pool = await get_pool()
    if not pool: return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM stays WHERE id = $1", stay_id)
        return dict(row) if row else None

# ─── Bookings & Transactions (Phase 5) ───────────────────────────────
async def create_booking(user_id: str, item_id: str, item_type: str, check_in=None, check_out=None, total_price=0.0):
    pool = await get_pool()
    if not pool:
        return {"status": "pending", "id": "B-MOCK"}

    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO bookings (user_id, item_id, item_type, check_in, check_out, total_price, status, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, 'pending', NOW())
            RETURNING *
            """,
            user_id, item_id, item_type, check_in, check_out, total_price
        )
        return dict(row) if row else {"id": "B-FAIL", "status": "error"}

async def fetch_user_bookings(user_id: str):
    pool = await get_pool()
    if not pool: return []
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM bookings WHERE user_id = $1 ORDER BY created_at DESC", user_id)
        return [dict(row) for row in rows]

# ─── OHA Aggregator (Merchants) (Phase 5) ───────────────────────────────
async def register_discovered_merchant(name: str, lga_id: str, source: str = 'crawler', contact: str = None):
    pool = await get_pool()
    if not pool: return {"id": "M-MOCK"}
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO merchants (business_name, lga_id, discovery_source, contact_phone, status, created_at)
            VALUES ($1, $2, $3, $4, 'discovered', NOW())
            RETURNING *
            """,
            name, lga_id, source, contact
        )
        return dict(row) if row else None

async def fetch_merchants(lga_id: str = None, status: str = None):
    pool = await get_pool()
    if not pool: return []
    async with pool.acquire() as conn:
        query = "SELECT * FROM merchants"
        params = []
        if lga_id or status:
            query += " WHERE TRUE"
            if lga_id:
                params.append(lga_id)
                query += f" AND lga_id = ${len(params)}"
            if status:
                params.append(status)
                query += f" AND status = ${len(params)}"
        
        rows = await conn.fetch(query, *params)
        return [dict(row) for row in rows]

# ─── Governance (Tax & Levy) (Phase 5) ───────────────────────────────
async def record_tourism_levy(booking_id: str, merchant_id: str, amount: float):
    pool = await get_pool()
    if not pool: return True
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO tax_records (booking_id, merchant_id, levy_amount, status, created_at) VALUES ($1, $2, $3, 'pending', NOW())",
            booking_id, merchant_id, amount
        )
    return True

# ─── OEMG Events (Phase 5) ───────────────────────────────
async def fetch_events(lga_id: str = None, category: str = None, status: str = 'verified'):
    pool = await get_pool()
    if not pool: return []
    async with pool.acquire() as conn:
        query = "SELECT * FROM events WHERE TRUE"
        params = []
        if lga_id:
            params.append(lga_id)
            query += f" AND lga_id = ${len(params)}"
        if category:
            params.append(category)
            query += f" AND category = ${len(params)}"
        if status:
            params.append(status)
            query += f" AND status = ${len(params)}"
            
        rows = await conn.fetch(query + " ORDER BY event_date ASC", *params)
        return [dict(row) for row in rows]

async def create_event(data: dict):
    pool = await get_pool()
    if not pool: return None
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO events (title, description, event_date, lga_id, venue, category, ticket_price, merchant_id, status)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
            RETURNING *
            """,
            data.get("title"), data.get("description"), data.get("event_date"),
            data.get("lga_id"), data.get("venue"), data.get("category"),
            data.get("ticket_price", 0.0), data.get("merchant_id"), data.get("status", 'discovered')
        )
        return dict(row) if row else None

async def issue_ticket(user_id: str, event_id: str, booking_id: str = None):
    pool = await get_pool()
    if not pool: return {"qr_code": "QR-MOCK"}
    import uuid
    qr = f"ISEYAA-TKT-{uuid.uuid4().hex[:8].upper()}"
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO tickets (user_id, event_id, booking_id, qr_code, status) VALUES ($1, $2, $3, $4, 'valid')",
            user_id, event_id, booking_id, qr
        )
    return {"qr_code": qr}

# ─── MSSI (Media Signals & Social Intelligence) (Phase 5) ───────────────────
async def log_media_signal(source: str, summary: str, sentiment: float, lga_id: str = None, metadata: dict = None):
    pool = await get_pool()
    if not pool: return True
    async with pool.acquire() as conn:
        import json
        await conn.execute(
            """
            INSERT INTO media_signals (source_type, content_summary, sentiment_score, lga_id, metadata, created_at)
            VALUES ($1, $2, $3, $4, $5, NOW())
            """,
            source.lower(), summary, sentiment, lga_id, json.dumps(metadata or {})
        )
    return True

async def fetch_signals(limit: int = 20):
    pool = await get_pool()
    if not pool: return []
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM media_signals ORDER BY created_at DESC LIMIT $1", limit)
        return [dict(row) for row in rows]

async def fetch_regional_sentiment(lga_id: str):
    pool = await get_pool()
    if not pool: return 0.0
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT AVG(sentiment_score) as avg_sentiment FROM media_signals WHERE lga_id = $1", lga_id)
        return row["avg_sentiment"] if row and row["avg_sentiment"] else 0.0
