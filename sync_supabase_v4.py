import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

SYNC_SQL_V4 = """
-- ISEYAA MASTER SECURE AUTH (Launch 2.1: Identity Pillar 13)

-- 13. Identity & Secure Registry (Pillar 13)
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    full_name TEXT,
    role TEXT DEFAULT 'traveler', -- traveler, host, government, admin
    kyc_status TEXT DEFAULT 'unverified', -- unverified, pending, verified
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Ensure registrations are tracked
CREATE TABLE IF NOT EXISTS user_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    token TEXT NOT NULL,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add foreign key to kyc_submissions if not exists
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name='kyc_submissions' AND column_name='user_id') THEN
        ALTER TABLE kyc_submissions ADD COLUMN user_id UUID REFERENCES users(id) ON DELETE CASCADE;
    END IF;
END $$;
"""

async def sync():
    print("ISEYAA Master Sync 4.0 — Deploying Secure Identity Registry...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected to Supabase. Deploying Pillar 13 Extensions...")
        await conn.execute(SYNC_SQL_V4)
        print("Sync Successful! Secure Identity Registry (Login/Register) is now OPERATIONAL.")
        await conn.close()
    except Exception as e:
        print(f"Sync Failed: {e}")

if __name__ == "__main__":
    asyncio.run(sync())
