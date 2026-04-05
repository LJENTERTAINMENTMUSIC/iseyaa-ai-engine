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
        
        migration_dir = "../../supabase/migrations"
        migration_files = sorted([f for f in os.listdir(migration_dir) if f.endswith(".sql")])
        
        for migration_file in migration_files:
            print(f"Running migration: {migration_file}...")
            with open(os.path.join(migration_dir, migration_file), "r", encoding="utf-8") as f:
                sql_query = f.read()
            await conn.execute(sql_query)
            print(f"Migration {migration_file} completed!")

        print("Database successfully seeded and migrated!")
        await conn.close()
    except Exception as e:
        print(f"Migration failed: {e}")

if __name__ == "__main__":
    asyncio.run(run_migration())
