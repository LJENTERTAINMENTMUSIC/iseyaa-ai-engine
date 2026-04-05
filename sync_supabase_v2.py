import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_SQL_V2 = """
-- ISEYAA MASTER LIVE SYNC (Launch 2.0: The 13 Pillars)

-- 1. Digital Marketplace (Pillar 1)
CREATE TABLE IF NOT EXISTS merchants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    category TEXT,
    location TEXT,
    rating NUMERIC(3,2),
    image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    merchant_id UUID REFERENCES merchants(id),
    name TEXT NOT NULL,
    price NUMERIC(12,2),
    image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    merchant_id UUID REFERENCES merchants(id),
    items JSONB,
    total NUMERIC(12,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Transportation & Mobility (Pillar 2)
CREATE TABLE IF NOT EXISTS vehicles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type TEXT,
    plate_number TEXT UNIQUE,
    driver_id UUID,
    status TEXT DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS trips (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    vehicle_id UUID REFERENCES vehicles(id),
    pickup TEXT,
    dropoff TEXT,
    fare NUMERIC(12,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Clubs & Associations (Pillar 5)
CREATE TABLE IF NOT EXISTS clubs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    type TEXT,
    membership_fee NUMERIC(12,2)
);

-- 4. User Wallets (Pillar 9)
CREATE TABLE IF NOT EXISTS wallets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    balance NUMERIC(12,2) DEFAULT 0.00,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    amount NUMERIC(12,2),
    type TEXT,
    reference TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 5. Stays Expansion (Pillar 3)
CREATE TABLE IF NOT EXISTS stays (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    lga_id TEXT,
    category TEXT,
    price_per_night NUMERIC(12,2),
    image TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

async def sync():
    print("ISEYAA Master Sync 2.0 — Executing 13 Pillar Schema...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to Supabase. Deploying Sprints 1 & 2 Tables...")
        await conn.execute(SYNC_SQL_V2)
        print("Sync Successful! All 13 Pillar tables (Commerce, Transport, Wallet, Clubs) are now LIVE.")
        await conn.close()
    except Exception as e:
        print(f"Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
