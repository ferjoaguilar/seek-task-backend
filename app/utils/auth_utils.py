import datetime
import os

from fastapi import HTTPException, status
from app.schemas.auth_schema import TokenType
import jwt

SECRETS = {
    TokenType.ACCESS: os.getenv("JWT_SECRET_ACCESS"),
}


def generate_jwt(payload: dict, secret: str, tokenType: TokenType, expires: int) -> str:
    payload.update({"iss": "seek_backend", 
                    "sub": tokenType.value,
                    "iat": datetime.datetime.now(tz=datetime.timezone.utc), 
                    "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=expires)})
    return jwt.encode(payload, secret, algorithm="HS256")

def verify_jwt(token: str, tokenType: TokenType) -> dict:
    secret = SECRETS.get(tokenType)
    if not secret:
        raise ValueError("Invalid token type")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"], options={"verify_signature": True})
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    except Exception as e:
        raise e