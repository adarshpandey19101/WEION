from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import time
from datetime import datetime
from api.database import get_db
from api.models import Goal
from api.system import add_log

from api.auth import get_api_key

router = APIRouter(prefix="/api/goals", tags=["Goals"], dependencies=[Depends(get_api_key)])

@router.get("/")
def get_goals(db: Session = Depends(get_db)):
    """Get all goals from DB"""
    goals = db.query(Goal).all()
    return goals

@router.post("/")
async def create_goal(goal_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new goal in DB"""
    goal = Goal(
        id=f"goal-{int(time.time()*1000)}",
        title=goal_data.get("title", ""),
        description=goal_data.get("description", ""),
        status=goal_data.get("status", "not-started"),
        priority=goal_data.get("priority", "medium"),
        progress=goal_data.get("progress", 0),
        deadline=goal_data.get("deadline"),
        createdAt=datetime.now().isoformat()
    )
    db.add(goal)
    db.commit()
    db.refresh(goal)
    await add_log("info", f"Goal created: {goal.title}", db)
    return goal

@router.patch("/{goal_id}")
async def update_goal(goal_id: str, updates: Dict[str, Any], db: Session = Depends(get_db)):
    """Update a goal in DB"""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        for key, value in updates.items():
            setattr(goal, key, value)
        db.commit()
        db.refresh(goal)
        await add_log("info", f"Goal updated: {goal_id}", db)
        return goal
    raise HTTPException(status_code=404, detail="Goal not found")

@router.delete("/{goal_id}")
async def delete_goal(goal_id: str, db: Session = Depends(get_db)):
    """Delete a goal by ID from DB"""
    goal = db.query(Goal).filter(Goal.id == goal_id).first()
    if goal:
        db.delete(goal)
        db.commit()
        await add_log("info", f"Goal deleted: {goal_id}", db)
        return {"message": "Goal deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Goal not found")
