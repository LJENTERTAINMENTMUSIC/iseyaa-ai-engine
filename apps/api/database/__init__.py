import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

async def get_db_conn():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL not found in environment.")
    return await asyncpg.connect(DATABASE_URL)

async def search_destinations(q: str):
    conn = await get_db_conn()
    try:
        results = await conn.fetch(
            "SELECT * FROM destinations WHERE title ILIKE $1 OR location ILIKE $1",
            f"%{q}%"
        )
        return [dict(r) for r in results]
    finally:
        await conn.close()

async def get_timestamp():
    from datetime import datetime
    return datetime.now().isoformat()
