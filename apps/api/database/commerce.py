from . import get_db_conn

async def get_merchants(category=None):
    conn = await get_db_conn()
    try:
        # Pillar 1: Digital Marketplace
        query = "SELECT * FROM merchants WHERE 1=1"
        params = []
        if category:
            params.append(category)
            query += f" AND category = ${len(params)}"
        
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def get_products(merchant_id=None):
    conn = await get_db_conn()
    try:
        # Pillar 1: Digital Marketplace
        query = "SELECT * FROM products WHERE 1=1"
        params = []
        if merchant_id:
            params.append(merchant_id)
            query += f" AND merchant_id = $1"
            
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def create_order(user_id, merchant_id, items, total):
    conn = await get_db_conn()
    try:
        # Pillar 1: Digital Marketplace
        row = await conn.fetchrow(
            """
            INSERT INTO orders (user_id, merchant_id, items, total, status)
            VALUES ($1, $2, $3, $4, 'pending')
            RETURNING *
            """,
            user_id, merchant_id, items, total
        )
        return dict(row)
    finally:
        await conn.close()

async def record_commission(order_id, amount):
    conn = await get_db_conn()
    try:
        # Pillar 1: Digital Marketplace (OHA Revenue Share)
        await conn.execute(
            "INSERT INTO tax_records (order_id, levy_amount, status) VALUES ($1, $2, 'pending')",
            order_id, amount
        )
    finally:
        await conn.close()
