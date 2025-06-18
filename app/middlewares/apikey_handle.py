import os
from fastapi import HTTPException, Security
from fastapi.security import api_key


api_key_header = api_key.APIKeyHeader(name='X-API-Key', auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == os.getenv("SECRET_ACCESS_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=401, detail="Unauthorized Access Key")