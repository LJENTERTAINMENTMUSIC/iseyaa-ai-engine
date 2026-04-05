import sys
import os
import json
from pathlib import Path

# Add project root and packages to path
root = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root / "apps" / "api"))
sys.path.append(str(root / "packages"))

def test_kyc_flow():
    print("--- Testing KYC Phase 3 Flow ---")
    try:
        from main import app
        from fastapi.testclient import TestClient
        client = TestClient(app)
        
        # 1. Test KYC Upload
        payload = {
            "user_id": "test_user_p3",
            "document_type": "passport",
            "document_number": "A1234567",
            "file_url": "https://storage.iseyaa.ng/docs/p_test.jpg"
        }
        resp = client.post("/api/kyc/upload", json=payload)
        print(f"KYC Upload Status: {resp.status_code}")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "processing"
        print(f"Tracking ID Generated: {data['tracking_id']}")
        
        # 2. Test KYC Status
        resp = client.get("/api/kyc/status/test_user_p3")
        print(f"KYC Status Check: {resp.status_code}")
        assert resp.status_code == 200
        assert resp.json()["status"] == "processing"
        
        # 3. Test AI Agent Link
        ai_resp = client.post("/api/ai/concierge", json={"query": "Who is the Alake of Egbaland?"})
        print(f"AI Concierge Status: {ai_resp.status_code}")
        assert ai_resp.status_code == 200
        assert ai_resp.json()["mode"] == "agent"
        
        print("✅ ALL PHASE 3 SMOKE TESTS PASSED")
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Create mock .env variables if not present for the test
    os.environ["DATABASE_URL"] = "" # Use fallback
    os.environ["AI_PROVIDER"] = "mock"
    test_kyc_flow()
