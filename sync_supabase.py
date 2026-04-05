import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_SQL = """
-- ISEYAA MASTER LIVE SYNC (Launch 1.0)
-- 1. Create Bookings & Transactions (Monetization Node)
CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    item_id TEXT NOT NULL,
    item_type TEXT NOT NULL,
    check_in DATE,
    check_out DATE,
    total_price NUMERIC(12,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Create Tax Records (OHA/Governance Node)
CREATE TABLE IF NOT EXISTS tax_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_id UUID REFERENCES bookings(id),
    merchant_id TEXT,
    levy_amount NUMERIC(12,2),
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Create Media Signals (MSSI Intelligence Node)
CREATE TABLE IF NOT EXISTS media_signals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_type TEXT,
    content_summary TEXT,
    sentiment_score NUMERIC(3,2),
    lga_id TEXT,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Create KYC Submissions (Identity Node)
CREATE TABLE IF NOT EXISTS kyc_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    document_type TEXT,
    document_number TEXT,
    file_url TEXT,
    tracking_id TEXT UNIQUE,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
"""

async def sync():
    print("ISEYAA Master Sync — Executing Launch 1.0 Schema...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected. Running SQL...")
        await conn.execute(SYNC_SQL)
        print("Sync Successful! All Production Tables are now LIVE.")
        await conn.close()
    except Exception as e:
        print(f"Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
