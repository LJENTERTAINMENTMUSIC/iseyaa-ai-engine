import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def test_conn():
    print("ISEYAA connectivity check (Supabase)...")
    if not DATABASE_URL:
        print("Error: DATABASE_URL not found in .env")
        return

    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connection Successful!")
        
        # Check for core tables
        tables = ["lga_profiles", "destinations", "bookings", "tax_records", "media_signals"]
        for table in tables:
            try:
                row = await conn.fetchval(f"SELECT count(*) FROM {table}")
                print(f"Table {table}: OK ({row} rows)")
            except Exception:
                print(f"Table {table}: MISSING")
        
        await conn.close()
    except Exception as e:
        print(f"Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_conn())
