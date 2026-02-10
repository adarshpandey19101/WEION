
# backend/routers/governance.py

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any, List
import yaml
import os
import sys

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.database import SessionLocal
from api.models import GovernanceVote

router = APIRouter(
    prefix="/api/governance",
    tags=["governance"],
    responses={404: {"description": "Not found"}},
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/constitution")
async def get_constitution():
    """
    Returns the Immutable Civilization Constitution.
    """
    const_path = "civilization/constitution.yaml"
    if not os.path.exists(const_path):
        raise HTTPException(status_code=404, detail="Constitution not found.")
        
    with open(const_path, "r") as f:
        data = yaml.safe_load(f)
    return data

@router.get("/votes")
async def get_recent_votes(limit: int = 10, db = Depends(get_db)):
    """
    Returns recent Council Votes (Human, AI, Tech, Econ).
    """
    votes = db.query(GovernanceVote).order_by(GovernanceVote.timestamp.desc()).limit(limit).all()
    return votes
