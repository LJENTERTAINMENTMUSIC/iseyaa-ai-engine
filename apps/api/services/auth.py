import os
import jwt
from fastapi import Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

# SUPABASE_JWT_SECRET is required to verify real user sessions
# This is usually found in the Supabase Dashboard -> Settings -> API
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "iseyaa-placeholder-secret")

async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        # Fallback for mock/local development if no token provided
        if os.getenv("ENVIRONMENT") == "development":
             return {"user_id": "mock-dev-user", "role": "traveler", "kyc_status": "unverified"}
        raise HTTPException(status_code=401, detail="Missing or invalid authentication token")

    token = auth_header.split(" ")[1]
    try:
        # Supabase uses HS256 for JWTs by default
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"], audience="authenticated")
        
        # Supabase JWT Payload usually contains:
        # sub (user_id), email, role, user_metadata
        user_id = payload.get("sub")
        role = payload.get("role", "authenticated") # Supabase role is usually 'authenticated'
        
        # We map this to our internal ISEYAA roles
        # In a real scenario, we might query the 'users' table to get the full profile/role
        return {
            "user_id": user_id,
            "role": role,
            "email": payload.get("email"),
            "kyc_status": "pending" # We will verify this against the DB in the main logic
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authentication token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")
