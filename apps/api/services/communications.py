"""
Communications Service — ISEYAA State Operating System
Handles all merchant onboarding and traveler notifications.
"""

from typing import Dict, Any, List
import datetime

class CommunicationsService:
    def __init__(self):
        self.provider = "mock"
        self.sent_log = []

    async def send_discovery_invite(self, business_name: str, contact_info: str, lga: str):
        # In Phase 5, this would use SendGrid/Twilio.
        # For the prototype, we log the message and trigger a console print for governance audit.
        message = f"""
        Dear {business_name} Owner,
        Your business in {lga} has been discovered by the Ogun State Tourism Intelligence Node (ISEYAA).
        
        To verify your business and begin accepting bookings via the State Operating System:
        Click here: https://iseyaa.og.gov.ng/verify?name={business_name.replace(' ', '+')}
        
        Benefits:
        - Global visibility on ISEYAA Host & Traveler apps.
        - Automated Tax & Levy compliance.
        - Verified Merchant badge.
        """
        
        timestamp = datetime.datetime.now().isoformat()
        self.sent_log.append({
            "to": contact_info, "type": "discovery_email", 
            "business": business_name, "timestamp": timestamp
        })
        
        print(f"[COMMUNICATIONS] Sent discovery invite to {business_name} at {contact_info}.")
        return {"status": "sent", "tracking_id": f"MSG-{timestamp[:10]}"}

    async def notify_booking_escrow(self, merchant_id: str, booking_id: str, total_price: float):
        # Notify the host that a guest has booked and funds are held in state escrow.
        pass

# Singleton instance
comm_service = CommunicationsService()
