from typing import List, Dict, Any
from datetime import datetime
import time
from fastapi import WebSocket

# ==================== GLOBAL STATE ====================
SYSTEM_STATE = {
    "state": "idle",  # idle, running, paused, error
    "goal": "No goal set",
    "uptime": 0,
    "activeAgents": 0,
    "errorRate": 0.0,
    "startTime": None,
}

# WebSocket connection managers
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

task_manager = ConnectionManager()
log_manager = ConnectionManager()

async def add_log(level: str, message: str, db=None):
    """Add a log entry and broadcast to WebSocket clients"""
    # Import here to avoid circular dependency if models import this file
    from api.models import Log
    
    if db:
        log_entry = Log(
            level=level, 
            message=message, 
            timestamp=datetime.now().isoformat()
        )
        db.add(log_entry)
        db.commit()
    
    # Broadcast
    await log_manager.broadcast({
        "type": "log",
        "data": {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
    })

async def add_task_broadcast(task_data: Dict[str, Any]):
    """Broadcast task updates to WebSocket clients"""
    await task_manager.broadcast({
        "type": "task_update",
        "data": task_data
    })
