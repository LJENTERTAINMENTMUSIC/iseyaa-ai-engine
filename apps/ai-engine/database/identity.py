from . import get_db_conn

async def submit_kyc(user_id, doc_type, doc_num, file_url):
    conn = await get_db_conn()
    try:
        # Pillar 13: Security & Identity
        row = await conn.fetchrow(
            """
            INSERT INTO kyc_submissions (user_id, document_type, document_number, file_url, status)
            VALUES ($1, $2, $3, $4, 'pending')
            RETURNING *
            """,
            user_id, doc_type, doc_num, file_url
        )
        return dict(row)
    finally:
        await conn.close()

async def get_kyc_status(user_id):
    conn = await get_db_conn()
    try:
        # Pillar 13: Security & Identity
        status = await conn.fetchval(
            "SELECT status FROM kyc_submissions WHERE user_id = $1 ORDER BY created_at DESC LIMIT 1",
            user_id
        )
        return status or "not_started"
    finally:
        await conn.close()
