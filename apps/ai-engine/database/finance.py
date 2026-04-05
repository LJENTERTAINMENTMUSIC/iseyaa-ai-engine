from . import get_db_conn

async def get_user_balance(user_id):
    conn = await get_db_conn()
    try:
        # Pillar 9: User Wallet
        balance = await conn.fetchval(
            "SELECT balance FROM wallets WHERE user_id = $1",
            user_id
        )
        return balance or 0.00
    finally:
        await conn.close()

async def get_user_transactions(user_id):
    conn = await get_db_conn()
    try:
        # Pillar 9: User Wallet
        rows = await conn.fetch(
            "SELECT * FROM transactions WHERE user_id = $1 ORDER BY created_at DESC",
            user_id
        )
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def record_transaction(user_id, amount, type, reference, status='pending'):
    conn = await get_db_conn()
    try:
        # Pillar 9: User Wallet
        row = await conn.fetchrow(
            """
            INSERT INTO transactions (user_id, amount, type, reference, status)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
            """,
            user_id, amount, type, reference, status
        )
        return dict(row)
    finally:
        await conn.close()
