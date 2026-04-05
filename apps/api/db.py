# ISEYAA Unified Database Node (Launch 2.0)
# This module provides a unified interface for all 13 Functional Pillars

from database.__init__ import get_db_conn, search_destinations, get_timestamp
from database.identity import submit_kyc, get_kyc_status
from database.hospitality import get_destinations, get_stays, create_booking, record_tax_levy
from database.commerce import get_merchants, get_products, create_order, record_commission
from database.finance import get_user_balance, get_user_transactions, record_transaction

# ─── Legacy Compatibility (if needed) ──────────────────────────────────────────
async def get_all_destinations():
    return await get_destinations()

async def get_all_stays():
    return await get_stays()
