from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from api.database import get_db
from api.models import Setting
from api.system import add_log

from api.auth import get_api_key

router = APIRouter(prefix="/api/settings", tags=["Settings"], dependencies=[Depends(get_api_key)])

DEFAULT_SETTINGS = {
    "model": "qwen2.5:7b",
    "timeout": 120,
    "notifications": True,
    "soundEffects": False,
    "theme": "dark",
    "apiKey": ""
}

@router.get("/")
def get_settings(db: Session = Depends(get_db)):
    """Get current settings from DB, merge with defaults"""
    db_settings = db.query(Setting).all()
    settings_dict = DEFAULT_SETTINGS.copy()
    
    for s in db_settings:
        settings_dict[s.key] = s.value
        
    return settings_dict

@router.patch("/")
async def update_settings(updates: Dict[str, Any], db: Session = Depends(get_db)):
    """Update settings in DB"""
    for key, value in updates.items():
        setting = db.query(Setting).filter(Setting.key == key).first()
        if not setting:
            setting = Setting(key=key, value=value)
            db.add(setting)
        else:
            setting.value = value
    db.commit()
    await add_log("info", f"Settings updated: {list(updates.keys())}", db)
    
    return get_settings(db)
