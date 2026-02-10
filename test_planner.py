
# test_planner.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from agents.planner import make_plan
from api.database import SessionLocal
from api.models import PlannerLog

def test_planner_execution():
    print("--- Testing Planner Upgrade ---")
    task = "Analyze the recent logs and summarize any errors."
    
    print(f"Task: {task}")
    
    try:
        # Run Planner
        plan = make_plan(task)
        
        print("\n--- Plan Output (Pydantic) ---")
        print(plan.model_dump_json(indent=2))
        
        # Verify DB Log
        db = SessionLocal()
        log_entry = db.query(PlannerLog).order_by(PlannerLog.id.desc()).first()
        
        print("\n--- DB Log Verification ---")
        if log_entry:
            print(f"ID: {log_entry.id}")
            print(f"Confidence: {log_entry.confidence}")
            print(f"Successful: {log_entry.successful}")
            print(f"Planner Version: {log_entry.planner_version}")
            if log_entry.user_input == task:
                print("✅ Log matches task input")
            else:
                print("❌ Log input mismatch")
        else:
            print("❌ No log entry found!")
        
        db.close()
        
    except Exception as e:
        print(f"❌ Test Failed: {e}")

if __name__ == "__main__":
    test_planner_execution()
