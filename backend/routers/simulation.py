
# backend/routers/simulation.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from simulation.sandbox_controller import SandboxController

router = APIRouter(
    prefix="/api/simulation",
    tags=["simulation"],
    responses={404: {"description": "Not found"}},
)

class SimulationRequest(BaseModel):
    decision: str
    duration_steps: int = 50

@router.post("/run")
async def run_simulation(request: SimulationRequest):
    """
    Runs a Civilization Sandbox simulation.
    Input: Proposed Decision.
    Output: Narrative history, Risk Report, Timeline Data.
    """
    try:
        controller = SandboxController()
        report = controller.run_simulation(request.decision, request.duration_steps)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
