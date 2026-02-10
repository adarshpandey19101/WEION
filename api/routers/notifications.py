from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import time
from datetime import datetime
from api.database import get_db
from api.models import Notification

from api.auth import get_api_key

router = APIRouter(prefix="/api/notifications", tags=["Notifications"], dependencies=[Depends(get_api_key)])

@router.get("/")
def get_notifications(db: Session = Depends(get_db)):
    """Get all notifications from DB"""
    notifications = db.query(Notification).all()
    if not notifications:
        return [
            {
                "id": "notif-init",
                "type": "info",
                "title": "System Started",
                "message": "WEION AI system initialized with persistent storage",
                "timestamp": datetime.now().isoformat(),
                "read": False
            }
        ]
    return notifications

@router.post("/")
async def create_notification(notif_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a notification in DB"""
    notif = Notification(
        id=f"notif-{int(time.time()*1000)}",
        type=notif_data.get("type", "info"),
        title=notif_data.get("title", ""),
        message=notif_data.get("message", ""),
        timestamp=datetime.now().isoformat(),
        read=False
    )
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif

@router.patch("/{notif_id}/read")
def mark_notification_read(notif_id: str, db: Session = Depends(get_db)):
    """Mark notification as read in DB"""
    notif = db.query(Notification).filter(Notification.id == notif_id).first()
    if notif:
        notif.read = True
        db.commit()
        db.refresh(notif)
        return notif
    raise HTTPException(status_code=404, detail="Notification not found")

@router.delete("/")
def clear_notifications(db: Session = Depends(get_db)):
    """Clear all notifications from DB"""
    db.query(Notification).delete()
    db.commit()
    return {"message": "All notifications cleared"}
