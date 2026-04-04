import asyncio
import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

async def run_migration():
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        print("DATABASE_URL is missing!")
        return

    print("Connecting to Supabase Database...")
    try:
        conn = await asyncpg.connect(database_url)
        print("Connected successfully.")
        
        print("Reading SQL migration file...")
        with open("../supabase/migrations/001_create_destinations.sql", "r", encoding="utf-8") as f:
            sql_query = f.read()

        print("Pushing database schema and data...")
        await conn.execute(sql_query)
        print("Database successfully seeded!")
        
        await conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_migration())
