from fastapi import APIRouter
from datetime import datetime
import uuid

from api.schema import (
    QueryRequest, QueryResponse,
    Task, MemoryItem, Goal
)
from api.ollama_client import run_llm

router = APIRouter()

# ------------------ STATE ------------------
SYSTEM_STATE = {
    "running": False,
    "start_time": None
}

TASKS = []
MEMORY = []
GOALS = []

# ------------------ CORE ------------------
@router.get("/status")
def status():
    return {
        "state": "running" if SYSTEM_STATE["running"] else "idle",
        "startTime": SYSTEM_STATE["start_time"],
        "activeAgents": 3,
        "errorRate": 0.0,
    }


@router.post("/query", response_model=QueryResponse)
def query(req: QueryRequest):
    answer = run_llm(req.input)
    return {"answer": answer}


# ------------------ AUTONOMY ------------------
@router.post("/start")
def start():
    SYSTEM_STATE["running"] = True
    SYSTEM_STATE["start_time"] = datetime.utcnow()
    return {"status": "started"}


@router.post("/stop")
def stop():
    SYSTEM_STATE["running"] = False
    return {"status": "stopped"}


# ------------------ TASKS ------------------
@router.get("/tasks")
def get_tasks(filter: str = "all"):
    if filter == "all":
        return TASKS
    return [t for t in TASKS if t["status"] == filter]


# ------------------ MEMORY ------------------
@router.get("/memory")
def get_memory():
    return MEMORY


@router.post("/memory")
def add_memory(item: MemoryItem):
    MEMORY.append(item.dict())
    return {"status": "stored"}


@router.delete("/memory/{memory_id}")
def delete_memory(memory_id: str):
    global MEMORY
    MEMORY = [m for m in MEMORY if m["id"] != memory_id]
    return {"status": "deleted"}


# ------------------ GOALS ------------------
@router.get("/goals")
def get_goals():
    return GOALS


@router.post("/goals")
def add_goal(goal: Goal):
    GOALS.append(goal.dict())
    return {"status": "created"}


@router.patch("/goals/{goal_id}")
def update_goal(goal_id: str, status: str):
    for g in GOALS:
        if g["id"] == goal_id:
            g["status"] = status
    return {"status": "updated"}


@router.delete("/goals/{goal_id}")
def delete_goal(goal_id: str):
    global GOALS
    GOALS = [g for g in GOALS if g["id"] != goal_id]
    return {"status": "deleted"}
