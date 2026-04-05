from fastapi import APIRouter, Depends, HTTPException, Body
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from services.auth import get_current_user, get_password_hash, verify_password, create_access_token
import db
from datetime import timedelta

router = APIRouter(prefix="/api/identity", tags=["Identity & Security"])

# ─── Pydantic Models ──────────────────────────────────────────────────────────
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class KycRequest(BaseModel):
    doc_type: str
    doc_num: str
    file_url: str

# ─── Auth Endpoints ──────────────────────────────────────────────────────────
@router.post("/register", response_model=Token)
async def register(req: UserRegister):
    # Pillar 13: Identity & Security (Registration Node)
    conn = await db.get_db_conn()
    try:
        # 1. Check if user exists
        existing = await conn.fetchrow("SELECT id FROM users WHERE email = $1", req.email)
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # 2. Hash password
        hashed_pw = get_password_hash(req.password)
        
        # 3. Create user
        user = await conn.fetchrow(
            "INSERT INTO users (email, hashed_password, full_name) VALUES ($1, $2, $3) RETURNING id, email, full_name, role, kyc_status",
            req.email, hashed_pw, req.full_name
        )
        
        # 4. Generate Token
        access_token = create_access_token(data={"sub": str(user["id"]), "email": user["email"], "role": user["role"]})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": dict(user)
        }
    finally:
        await conn.close()

@router.post("/login", response_model=Token)
async def login(req: UserLogin):
    # Pillar 13: Identity & Security (Login Node)
    conn = await db.get_db_conn()
    try:
        # 1. Fetch user
        user = await conn.fetchrow("SELECT * FROM users WHERE email = $1", req.email)
        if not user or not verify_password(req.password, user["hashed_password"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        
        # 2. Generate Token
        access_token = create_access_token(data={"sub": str(user["id"]), "email": user["email"], "role": user["role"]})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "full_name": user["full_name"],
                "role": user["role"],
                "kyc_status": user["kyc_status"]
            }
        }
    finally:
        await conn.close()

# ─── Standard Endpoints ──────────────────────────────────────────────────────
@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    return {"user": user}

@router.post("/kyc/submit")
async def submit_kyc(
    req: KycRequest,
    user: dict = Depends(get_current_user)
):
    # Pillar 13: Security & Identity
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        row = await conn.fetchrow(
            """
            INSERT INTO kyc_submissions (user_id, document_type, document_number, file_url, status)
            VALUES ($1, $2, $3, $4, 'pending')
            RETURNING *
            """,
            user_id, req.doc_type, req.doc_num, req.file_url
        )
        # Update user status
        await conn.execute("UPDATE users SET kyc_status = 'pending' WHERE id = $1", user_id)
        return dict(row)
    finally:
        await conn.close()

@router.get("/kyc/status")
async def get_kyc_status(user: dict = Depends(get_current_user)):
    user_id = user["id"] if "id" in user else user["user_id"]
    conn = await db.get_db_conn()
    try:
        status = await conn.fetchval("SELECT kyc_status FROM users WHERE id = $1", user_id)
        return {"status": status}
    finally:
        await conn.close()
