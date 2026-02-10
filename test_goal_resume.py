
# test_goal_resume.py
import sys
import os
import json
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import GoalExecution
from autonomy.resume_manager import resume_pending_goals

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def test_goal_resume():
    print("\n--- Test: Goal Persistence & Resume Logic ---")
    
    # 1. Setup: Create a "zombie" goal in DB
    # Simulating a goal with 3 tasks, where Task 0 is done.
    db = SessionLocal()
    try:
        zombie_goal = GoalExecution(
            objective="Build a Resume Test",
            context="Testing persistence",
            status="RUNNING",
            tasks=["Task 1 (Done)", "Task 2 (Pending)", "Task 3 (Pending)"],
            current_task_index=1, # Next task is index 1 (Task 2)
            results=[
                {"success": True, "verdict": {"accepted": True, "score": 1.0, "issues": []}}
            ] # Result for Task 0
        )
        db.add(zombie_goal)
        db.commit()
        db.refresh(zombie_goal)
        zombie_id = zombie_goal.id
        print(f"🧟 Created Zombie Goal ID: {zombie_id}")
        
    finally:
        db.close()

    # 2. Mock Execution
    # run_atomic_task needs to be patched
    # It should receive Task 2 and Task 3.
    
    with patch("autonomy.goal_engine.run_atomic_task") as mock_runner:
        
        # Configure Mock
        def mock_side_effect(task, extra_context=None):
            print(f"[Mock] Running {task}")
            if extra_context:
                 print(f"       Resume Flag: {extra_context.get('resume')}")
                 
            return {"success": True, "verdict": {"accepted": True, "score": 1.0}}
            
        mock_runner.side_effect = mock_side_effect
        
        # 3. Trigger Resume
        print("\n⚡ Triggering Resume Manager...")
        resume_pending_goals(auto=True)
        
        # 4. Verify
        # Expected calls: Task 2 and Task 3. Task 1 should NOT be called.
        
        calls = [c[0][0] for c in mock_runner.call_args_list]
        print(f"\nCalled Tasks: {calls}")
        
        if "Task 1 (Done)" in calls:
            print("❌ FAILURE: Task 1 was re-executed!")
        elif "Task 2 (Pending)" in calls and "Task 3 (Pending)" in calls:
            print("✅ SUCCESS: Resumed correctly from Task 2.")
        else:
            print("❌ FAILURE: Did not run expected tasks.")
            
        # Verify DB Status
        db = SessionLocal()
        final_goal = db.query(GoalExecution).filter(GoalExecution.id == zombie_id).first()
        print(f"\nFinal DB Status: {final_goal.status}")
        print(f"Final Progress: {final_goal.current_task_index}/{len(final_goal.tasks)}")
        print(f"Final Results Count: {len(final_goal.results) if final_goal.results else 0}")
        
        if final_goal.status == "COMPLETED":
             print("✅ Goal marked COMPLETED in DB.")
        else:
             print(f"❌ Goal status mismatch: {final_goal.status}")
             
        db.close()

if __name__ == "__main__":
    test_goal_resume()
