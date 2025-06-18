import os
from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.schemas.auth_schema import TokenType
from app.utils.auth_utils import verify_jwt

security = HTTPBearer()

async def authorization(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token and return payload"""
    if credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=403, detail={
            "message": "Invalid token",
            "error": "Invalid authentication scheme"
        })
    if not credentials.credentials:
        raise HTTPException(status_code=403, detail={
            "message": "Invalid token",
            "error": "Token is missing"
        }) 
    try:
        secret_key = os.getenv("JWT_SECRET_ACCESS")
        if not secret_key:
            raise HTTPException(status_code=500, detail="Secret JWT access key is not set")
        payload = verify_jwt(token=credentials.credentials, tokenType=TokenType.ACCESS)
        return payload
    except Exception as e:
        raise HTTPException(status_code=401, detail={
            "message": "Unauthorized",
            "error": f"Invalid token {str(e)}"
        })