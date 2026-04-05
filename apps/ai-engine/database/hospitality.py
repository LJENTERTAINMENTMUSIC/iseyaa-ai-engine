from . import get_db_conn

async def get_destinations(category=None, lga=None):
    conn = await get_db_conn()
    try:
        # Pillar 11: Tourism, Culture & Heritage
        query = "SELECT * FROM destinations WHERE 1=1"
        params = []
        if category and category != "All":
            params.append(category)
            query += f" AND category = ${len(params)}"
        if lga:
            params.append(lga)
            query += f" AND lga_id = ${len(params)}"
        
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def get_stays(category=None, lga=None, price_max=None):
    conn = await get_db_conn()
    try:
        # Pillar 3: Accommodation & Hospitality (Focus: Shortlet, Hotel, Resort)
        query = "SELECT * FROM stays WHERE 1=1"
        params = []
        if category and category != "All":
            params.append(category)
            query += f" AND category = ${len(params)}"
        if lga:
            params.append(lga)
            query += f" AND lga_id = ${len(params)}"
        if price_max:
            params.append(price_max)
            query += f" AND price_per_night <= ${len(params)}"
        
        rows = await conn.fetch(query, *params)
        return [dict(r) for r in rows]
    finally:
        await conn.close()

async def create_booking(user_id, item_id, item_type, total_price):
    conn = await get_db_conn()
    try:
        # Pillar 3 & 11: Monetization
        row = await conn.fetchrow(
            """
            INSERT INTO bookings (user_id, item_id, item_type, total_price, status)
            VALUES ($1, $2, $3, $4, 'pending')
            RETURNING *
            """,
            user_id, item_id, item_type, total_price
        )
        return dict(row)
    finally:
        await conn.close()

async def record_tax_levy(booking_id, levy_amount):
    conn = await get_db_conn()
    try:
        # Pillar 12: Government Command & Compliance (OHA Node)
        await conn.execute(
            "INSERT INTO tax_records (booking_id, levy_amount, status) VALUES ($1, $2, 'pending')",
            booking_id, levy_amount
        )
    finally:
        await conn.close()
