
# backend/routers/war_room.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio
import random
import datetime

router = APIRouter(
    prefix="/api/war_room",
    tags=["war_room"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()

AGENTS = ["LOGIC_CORE", "EMPATHY_ENGINE", "ETHICS_VALIDATOR", "SOVEREIGNTY_GUARD", "STRATEGIST"]
ACTIONS = ["ANALYZING", "FILTERING", "REJECTING", "OPTIMIZING", "QUERYING_MEMORY", "SIMULATING"]

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Simulate "Thinking" Stream
            # In a real system, this would hook into logging.Handler
            await asyncio.sleep(random.uniform(0.5, 2.0))
            
            agent = random.choice(AGENTS)
            action = random.choice(ACTIONS)
            log = f"{action} context from {agent}..."
            
            if agent == "SOVEREIGNTY_GUARD":
                log = "🔒 Checking Constitution compliance..."
            elif agent == "EMPATHY_ENGINE":
                log = "❤️ Integrating user emotional context..."
            
            payload = {
                "timestamp": datetime.datetime.now().isoformat(),
                "agent": agent,
                "log": log,
                "status": "ACTIVE"
            }
            
            await websocket.send_json(payload)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
