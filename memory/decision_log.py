# memory/decision_log.py
import json
from datetime import datetime

LOG_FILE = "memory/decisions.json"

def log_decision(task, verdict, issues):
    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "task": task,
        "accepted": verdict["accepted"],
        "score": verdict["score"],
        "issues": issues
    }

    try:
        with open(LOG_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(entry)

    with open(LOG_FILE, "w") as f:
        json.dump(data, f, indent=2)
