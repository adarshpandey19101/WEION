# ui/backend/app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from autonomy.autonomy_loop import autonomous_run
import threading

app = FastAPI()

# Allow browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SYSTEM_STATUS = {
    "running": False,
    "mode": None
}

@app.get("/")
def root():
    return {"status": "AI Dashboard Backend Running"}

@app.get("/status")
def status():
    return SYSTEM_STATUS

@app.post("/run/autonomy")
def run_autonomy():
    if SYSTEM_STATUS["running"]:
        return {"message": "System already running"}

    SYSTEM_STATUS["running"] = True
    SYSTEM_STATUS["mode"] = "AUTONOMY"

    def run():
        try:
            autonomous_run(
                context="Personal AI system for decision making and automation"
            )
        finally:
            SYSTEM_STATUS["running"] = False
            SYSTEM_STATUS["mode"] = None

    thread = threading.Thread(target=run)
    thread.start()

    return {"message": "Autonomy started"}
