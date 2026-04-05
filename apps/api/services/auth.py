import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Request, HTTPException
from dotenv import load_dotenv

load_dotenv()

# SUPABASE_JWT_SECRET is required to verify real user sessions
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET", "iseyaa-placeholder-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 Days

# ─── Password Hashing ────────────────────────────────────────────────────────
def get_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ─── JWT Generation ─────────────────────────────────────────────────────────
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({
        "exp": expire,
        "aud": "authenticated",
        "iss": "iseyaa-ai-engine"
    })
    encoded_jwt = jwt.encode(to_encode, SUPABASE_JWT_SECRET, algorithm=ALGORITHM)
    return encoded_jwt

# ─── Current User Dependency ─────────────────────────────────────────────────
async def get_current_user(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        if os.getenv("ENVIRONMENT") == "development":
             return {"user_id": "mock-dev-user", "role": "traveler", "kyc_status": "unverified"}
        raise HTTPException(status_code=401, detail="Missing or invalid authentication token")

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=[ALGORITHM], audience="authenticated")
        user_id = payload.get("sub")
        role = payload.get("role", "authenticated")
        
        return {
            "id": user_id,
            "user_id": user_id,
            "role": role,
            "email": payload.get("email"),
            "kyc_status": payload.get("kyc_status", "unverified")
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Authentication token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid authentication token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication error: {str(e)}")
