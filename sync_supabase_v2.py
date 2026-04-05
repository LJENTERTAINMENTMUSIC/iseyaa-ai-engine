import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_SQL_V2_1 = """
-- ISEYAA MASTER LIVE SYNC (Launch 2.1: The Mobility Cluster Expansion)

-- 2. Transportation & Mobility (Pillar 2) - SCHEMA REFINEMENT
-- Add category and metadata to trips for Flight/E-Bike support
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trips' AND column_name='category') THEN
        ALTER TABLE trips ADD COLUMN category TEXT DEFAULT 'car';
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='trips' AND column_name='metadata') THEN
        ALTER TABLE trips ADD COLUMN metadata JSONB DEFAULT '{}';
    END IF;
END $$;

-- Ensure vehicles has category as well
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='vehicles' AND column_name='category') THEN
        ALTER TABLE vehicles ADD COLUMN category TEXT DEFAULT 'car';
    END IF;
END $$;

-- 12. Arts, Culture & Creative Economy (Pillar 12)
CREATE TABLE IF NOT EXISTS creative_assets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    category TEXT, -- DigitalArt, Music, NFT, Heritage
    creator_id UUID,
    price NUMERIC(12,2),
    file_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

async def sync():
    print("ISEYAA Master Sync 2.1 — Refining Mobility & Arts Schema...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to Supabase. Deploying Mobility Category Extensions...")
        await conn.execute(SYNC_SQL_V2_1)
        print("Sync Successful! Mobility (Flights/E-Bikes) & Arts tables are now OPTIMIZED.")
        await conn.close()
    except Exception as e:
        print(f"Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
