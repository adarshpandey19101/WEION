from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import time
from datetime import datetime
from sqlalchemy.orm import Session

from api.database import SessionLocal, engine, Base
from api.models import Task, Log
from api.system import SYSTEM_STATE, task_manager, log_manager, add_log, add_task_broadcast
from autonomy.autonomy_loop import autonomous_run

# Import Routers
from api.routers import memories, goals, tasks, analytics, settings, notifications

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WEION AI API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(memories.router)
app.include_router(goals.router)
# Tasks router was minimal, I'll include it.
app.include_router(tasks.router) 
app.include_router(analytics.router)
app.include_router(settings.router)
app.include_router(notifications.router)

# Root Endpoints
@app.get("/")
def root():
    return {
        "name": "WEION AI API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/status")
def get_status():
    SYSTEM_STATE["uptime"] = int(time.time() - SYSTEM_STATE["startTime"]) if SYSTEM_STATE["startTime"] else 0
    return SYSTEM_STATE

# Autonomy Control Endpoints (Moved here or create autonomy router later. Keeping here for visibility)
@app.post("/start")
async def start_autonomy():
    if SYSTEM_STATE["state"] == "running":
        await add_log("warning", "Autonomy already running")
        return {"message": "Already running", "state": SYSTEM_STATE["state"]}
    
    SYSTEM_STATE["state"] = "running"
    SYSTEM_STATE["startTime"] = time.time()
    SYSTEM_STATE["activeAgents"] = 3
    
    if SYSTEM_STATE["goal"] == "No goal set":
        SYSTEM_STATE["goal"] = "Increase productivity and automate tasks"
    
    await add_log("info", "Autonomy started")
    
    # Start loop
    asyncio.create_task(autonomous_run(context="Personal AI system"))
    
    # Create initial task in DB
    db = SessionLocal()
    try:
        new_task = Task(
            id="task-init",
            name="Initialize system",
            description="Starting autonomous operations",
            status="running",
            confidence=0.95,
            startTime=datetime.now().isoformat(),
            subtasks=[]
        )
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        await add_task_broadcast({
            "id": new_task.id,
            "name": new_task.name,
            "description": new_task.description,
            "status": new_task.status,
            "confidence": new_task.confidence
        })
    finally:
        db.close()
    
    return {"message": "Autonomy started successfully", "state": SYSTEM_STATE["state"]}

@app.post("/stop")
async def stop_autonomy():
    if SYSTEM_STATE["state"] == "idle":
        return {"message": "Already stopped", "state": SYSTEM_STATE["state"]}
    
    SYSTEM_STATE["state"] = "idle"
    SYSTEM_STATE["activeAgents"] = 0
    SYSTEM_STATE["startTime"] = None
    await add_log("info", "Autonomy stopped")
    return {"message": "Autonomy stopped", "state": SYSTEM_STATE["state"]}

# WebSocket Endpoints
@app.websocket("/ws/tasks")
async def websocket_tasks(websocket: WebSocket):
    await task_manager.connect(websocket)
    try:
        # Send initial tasks
        db = SessionLocal()
        try:
            tasks_list = db.query(Task).all()
            data = [{c.name: getattr(t, c.name) for c in t.__table__.columns} for t in tasks_list]
            await websocket.send_json({"type": "initial_tasks", "data": data})
        finally:
            db.close()
            
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        task_manager.disconnect(websocket)

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await log_manager.connect(websocket)
    try:
        # Send initial logs
        db = SessionLocal()
        try:
            logs = db.query(Log).order_by(Log.id.desc()).limit(50).all()
            data = [{c.name: getattr(l, c.name) for c in l.__table__.columns} for l in logs]
            await websocket.send_json({"type": "initial_logs", "data": data[::-1]})
        finally:
            db.close()
            
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        log_manager.disconnect(websocket)

# Background Simulation
@app.on_event("startup")
async def startup_event():
    await add_log("info", "WEION AI Backend started (Modular)")
    asyncio.create_task(simulate_task_updates())

async def simulate_task_updates():
    await asyncio.sleep(5)
    task_count = 1
    while True:
        if SYSTEM_STATE["state"] == "running":
            task_count += 1
            db = SessionLocal()
            try:
                new_task = Task(
                    id=f"task-sim-{int(time.time())}",
                    name=f"Automated Task {task_count}",
                    description="Simulated background activity",
                    status="running",
                    confidence=0.88,
                    startTime=datetime.now().isoformat(),
                    subtasks=[]
                )
                db.add(new_task)
                db.commit()
                # Broadcast
                await add_task_broadcast({
                    "id": new_task.id,
                    "name": new_task.name,
                    "status": "running"
                })
                await add_log("info", f"Task {task_count} started")
            except Exception as e:
                print(f"Sim error: {e}")
            finally:
                db.close()
        await asyncio.sleep(10)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
