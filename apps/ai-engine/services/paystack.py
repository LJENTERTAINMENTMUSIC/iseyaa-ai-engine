import os
import httpx
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

PAYSTACK_SECRET_KEY = os.getenv("PAYSTACK_SECRET_KEY")
PAYSTACK_BASE_URL = "https://api.paystack.co"

class PaystackService:
    @staticmethod
    async def initialize_transaction(email: str, amount_naira: float, metadata: dict = None):
        """
        Initializes a Paystack transaction.
        Amount must be in kobo (Naira * 100).
        """
        if not PAYSTACK_SECRET_KEY:
             # Fallback for dev/missing key
             return {"status": True, "data": {"authorization_url": "https://checkout.paystack.com/mock-url", "reference": "MOCK-REF"}}

        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json"
        }
        
        # Convert to Kobo
        amount_kobo = int(float(amount_naira) * 100)
        
        payload = {
            "email": email,
            "amount": amount_kobo,
            "metadata": metadata or {},
            "callback_url": os.getenv("WEB_URL", "http://localhost:3000") + "/bookings/callback"
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{PAYSTACK_BASE_URL}/transaction/initialize",
                    json=payload,
                    headers=headers
                )
                res_data = response.json()
                if response.status_code == 200 and res_data.get("status"):
                    return res_data
                else:
                    raise HTTPException(status_code=400, detail=f"Paystack Error: {res_data.get('message')}")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Payment initialization failed: {str(e)}")

    @staticmethod
    async def verify_transaction(reference: str):
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{PAYSTACK_BASE_URL}/transaction/verify/{reference}",
                headers=headers
            )
            return response.json()

paystack_service = PaystackService()
