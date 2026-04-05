import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_SQL_V3 = """
-- ISEYAA MASTER LIVE SYNC (Phase 3: The Full 13 Pillars)

-- 3. Healthcare & Telemedicine (Pillar 3)
CREATE TABLE IF NOT EXISTS clinics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT, -- Public, Private, Primary
    lga_id TEXT,
    location TEXT,
    services JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS consultations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    clinic_id UUID REFERENCES clinics(id),
    type TEXT, -- In-person, Telemedicine
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Agriculture & Agri-Tech (Pillar 4)
CREATE TABLE IF NOT EXISTS farms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT, -- Crop, Livestock, Processing
    lga_id TEXT,
    size_hectares NUMERIC(12,2)
);

CREATE TABLE IF NOT EXISTS agri_logistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    shipment_type TEXT,
    origin TEXT,
    destination TEXT,
    status TEXT DEFAULT 'pending'
);

-- 5. Education & E-Learning (Pillar 5)
CREATE TABLE IF NOT EXISTS schools (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    level TEXT, -- Primary, Secondary, Tertiary
    lga_id TEXT
);

CREATE TABLE IF NOT EXISTS courses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    provider TEXT,
    enrolled_count INTEGER DEFAULT 0
);

-- 6. Power & Utilities (Pillar 6)
CREATE TABLE IF NOT EXISTS utility_bills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    utility_type TEXT, -- Power, Water
    amount NUMERIC(12,2),
    status TEXT DEFAULT 'unpaid',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 9. Waste Management (Pillar 9)
CREATE TABLE IF NOT EXISTS waste_collections (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    frequency TEXT,
    lga_id TEXT,
    status TEXT DEFAULT 'active'
);

-- 10. Safety & Security (Pillar 10)
CREATE TABLE IF NOT EXISTS emergency_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type TEXT,
    description TEXT,
    lga_id TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 12. Arts & Creative Economy (Pillar 12)
CREATE TABLE IF NOT EXISTS venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT, -- Theater, Gallery, Cinema
    lga_id TEXT
);
"""

async def sync():
    print("ISEYAA Master Sync 3.0 — Scaling to 13 Pillars...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to Supabase. Deploying Final Extension Tables...")
        await conn.execute(SYNC_SQL_V3)
        print("Sync Successful! All 13 Pillar tables (Health, Agri, Edu, Utilities, Waste, Security, Arts) are now LIVE.")
        await conn.close()
    except Exception as e:
        print(f"Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
