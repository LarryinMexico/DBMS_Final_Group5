# app/core/security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import requests
import os

# Clerk 設定
CLERK_ISSUER = "https://humble-bug-26.clerk.accounts.dev"
CLERK_JWKS_URL = f"{CLERK_ISSUER}/.well-known/jwks.json"

security = HTTPBearer()

def get_clerk_public_key(kid: str):
    jwks = requests.get(CLERK_JWKS_URL).json()
    for key in jwks["keys"]:
        if key["kid"] == kid:
            return key
    raise HTTPException(status_code=401, detail="Invalid 'kid' in token")

async def verify_jwt(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # 拿到 header 的 kid
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header["kid"]

        # 找對應的 public key
        key = get_clerk_public_key(kid)

        # 驗證 token
        payload = jwt.decode(
            token,
            key,
            algorithms=["RS256"],
            issuer=CLERK_ISSUER
        )

        return payload  # ✅ 拿到 user_id / email 等資訊
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid JWT token")
