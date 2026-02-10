from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from api.database import get_db
from api.models import Task

from api.auth import get_api_key

router = APIRouter(prefix="/tasks", tags=["Tasks"], dependencies=[Depends(get_api_key)])

@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    """Get all tasks from DB"""
    tasks = db.query(Task).all()
    return tasks
