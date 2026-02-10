
# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add parent directory to path to import core modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(
    title="WEION Civilization Engine API",
    description="API for the WEION governed intelligence system.",
    version="1.0.0"
)

# CORS (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"system": "WEION", "status": "OPERATIONAL", "phase": "CIVILIZATION_ENGINE"}

# Routers
from backend.routers import simulation, governance, war_room
app.include_router(simulation.router)
app.include_router(governance.router)
app.include_router(war_room.router)
