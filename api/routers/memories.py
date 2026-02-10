from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import time
from datetime import datetime
from api.database import get_db
from api.models import Memory
from api.system import add_log

from api.auth import get_api_key

router = APIRouter(prefix="/api/memories", tags=["Memory"], dependencies=[Depends(get_api_key)])

@router.get("/")
def get_memories(db: Session = Depends(get_db)):
    """Get all memory items from DB"""
    memories = db.query(Memory).all()
    return memories

@router.post("/")
async def create_memory(memory_data: Dict[str, Any], db: Session = Depends(get_db)):
    """Create a new memory in DB"""
    memory_id = f"mem-{int(time.time()*1000)}"
    memory = Memory(
        id=memory_id,
        title=memory_data.get("title", ""),
        content=memory_data.get("content", ""),
        tags=memory_data.get("tags", []),
        timestamp=datetime.now().isoformat()
    )
    db.add(memory)
    db.commit()
    db.refresh(memory)
    await add_log("info", f"Memory created: {memory.title}", db)
    return memory

@router.delete("/{memory_id}")
async def delete_memory(memory_id: str, db: Session = Depends(get_db)):
    """Delete a memory by ID from DB"""
    memory = db.query(Memory).filter(Memory.id == memory_id).first()
    if memory:
        db.delete(memory)
        db.commit()
        await add_log("info", f"Memory deleted: {memory_id}", db)
        return {"message": "Memory deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="Memory not found")
