from fastapi import Security, HTTPException, Depends
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN
from sqlalchemy.orm import Session
from api.database import get_db
from api.models import Setting
import os
from contextlib import contextmanager

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In a real scenario, this might come from env or DB. for now, DB or ENV.
# We'll check DB first, then ENV.

async def get_api_key(api_key_header: str = Security(api_key_header), db: Session = Depends(get_db)):
    # 1. Check if API key is set in Environment
    env_api_key = os.getenv("WEION_API_KEY")
    
    # 2. Check if API key is set in Database Settings
    db_setting = db.query(Setting).filter(Setting.key == "apiKey").first()
    db_api_key = db_setting.value if db_setting and db_setting.value else None
    
    # Logic:
    # If NO key is configured anywhere, we allow access (Development mode / First run)
    # If key IS configured, we require it.
    
    configured_key = env_api_key or db_api_key
    
    if not configured_key:
        return None # No auth required
        
    if api_key_header == configured_key:
        return api_key_header
        
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
    )
