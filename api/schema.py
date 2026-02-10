from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------- LLM ----------
class QueryRequest(BaseModel):
    input: str

class QueryResponse(BaseModel):
    answer: str


# ---------- TASKS ----------
class Task(BaseModel):
    id: str
    name: str
    status: str
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None


# ---------- MEMORY ----------
class MemoryItem(BaseModel):
    id: str
    content: str
    tags: List[str] = []
    created_at: datetime


# ---------- GOALS ----------
class Goal(BaseModel):
    id: str
    title: str
    description: str
    status: str  # not_started | running | completed


# ---------- PLANNER ----------
class PlannerStep(BaseModel):
    step_id: int
    action: str
    input: dict

class PlannerOutput(BaseModel):
    goal: str
    confidence: float
    steps: List[PlannerStep]
