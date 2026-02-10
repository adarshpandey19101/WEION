
# autonomy/resume_manager.py

import logging
from typing import List, Optional
from api.database import SessionLocal
from api.models import GoalExecution
from autonomy.goal_engine import run_goal_loop

# Initialize logger
logger = logging.getLogger(__name__)

def fetch_pending_goals(statuses: List[str] = None) -> List[GoalExecution]:
    """
    Fetches goals with specified statuses (default: RUNNING, PAUSED).
    """
    if statuses is None:
        statuses = ["RUNNING", "PAUSED"]
    
    db = SessionLocal()
    try:
        goals = db.query(GoalExecution).filter(GoalExecution.status.in_(statuses)).all()
        return goals
    finally:
        db.close()

def resume_pending_goals(auto: bool = True):
    """
    Finds and resumes pending goals.
    If auto=True, resumes them sequentially.
    """
    pending_goals = fetch_pending_goals()
    
    if not pending_goals:
        print("\n✅ No pending goals found. System clean.\n")
        return

    print(f"\n🔄 Found {len(pending_goals)} pending goals.")
    
    for goal in pending_goals:
        print(f"   - [ID {goal.id}] {goal.objective} (Status: {goal.status}, Progress: {goal.current_task_index}/{len(goal.tasks or [])})")

    if not auto:
        # In interactive mode (not implemented here fully), we might ask user.
        return

    print("\n🚀 Resuming pending goals...\n")
    
    for goal in pending_goals:
        try:
            # We pass resume_goal_id to run_goal_loop
            # run_goal_loop will refetch the fresh state from DB
            run_goal_loop(
                objective=goal.objective, # Optional if resuming
                context=goal.context,     # Optional if resuming
                resume_goal_id=goal.id
            )
        except Exception as e:
            print(f"❌ Failed to resume goal {goal.id}: {e}")
            logger.error(f"Resume Error: {e}")

if __name__ == "__main__":
    resume_pending_goals()
