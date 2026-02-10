
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.planner import make_plan
# from agents.researcher import research
# from agents.critic import critique
# from brain.model import ask_llm
# from control.evaluator import evaluate  # This was old LLM evaluator
# from control.rule_updater import update_rules

# from memory.decision_log import log_decision
# from memory.vector_store import add_memory, recall
# from memory.memory_agent import decide_memory

from autonomy.autonomy_loop import autonomous_run

# ================= CONFIG =================

TASK = "Explain first principles thinking."

import asyncio

MODE = "MANUAL"
# options: "MANUAL", "AUTONOMY"

MAX_RETRIES = 2

CONCEPTUAL_TASKS = [
    "thinking",
    "explain",
    "concept",
    "principle",
    "framework",
    "strategy",
    "philosophy"
]

# ================= HELPERS =================

def is_conceptual(task: str) -> bool:
    task_lower = task.lower()
    return any(word in task_lower for word in CONCEPTUAL_TASKS)


# ================= ATOMIC TASK RUNNER =================


# ================= ATOMIC TASK RUNNER =================
# Moved to brain/task_executor.py to avoid circular dependencies and promote reusability.
from brain.task_executor import run_atomic_task


# ================= MAIN =================

if __name__ == "__main__":

    print("\n================ START =================\n")
    
    # Ensure DB Tables Exist
    from api.database import engine, Base
    from api.models import GoalExecution, AtomicTaskCheckpoint # Import models to register them
    Base.metadata.create_all(bind=engine)
    
    # RESUME CHECK
    from autonomy.resume_manager import resume_pending_goals
    
    # 🔥 AUTONOMY MODE
    if MODE == "AUTONOMY":
        # Auto-resume in Autonomy Mode
        resume_pending_goals(auto=True)
        
        # --- PHASE 8: CEO DECISION HOOK ---
        from autonomy.decision_engine import decide_next_goal, apply_decision
        
        print("\n🧠 CEO THINKING: Arbitrating Goals...")
        decision = decide_next_goal()
        selected_goal_id = apply_decision(decision)
        
        if selected_goal_id:
             # Run the Selected Goal
             from autonomy.goal_engine import run_goal_loop
             
             # Fetch info to display (optional, run_goal_loop handles fetch)
             goal_result = run_goal_loop(objective="", resume_goal_id=selected_goal_id)
             
             # --- PHASE 17: LEARNING LOOP ---
             # If goal finished, analyze and learn
             if goal_result.get("status") in ["COMPLETED", "FAILED"]:
                 from autonomy.outcome_analyzer import analyze_outcome
                 from autonomy.weight_updater import update_priority_weights
                 
                 print("\n🧠 LEARNING: Analyzing Outcome...")
                 adjustments = analyze_outcome(selected_goal_id)
                 if adjustments:
                     update_priority_weights(adjustments)
             # -------------------------------
        else:
             print("\n💤 No actionable goals selected. System Idle.")

        # Continue with standard autonomous run if desired, or loop this
        # For now, we exit after one arbitration cycle to be safe, or we can loop.
        # As per request "System future me apni decision strategy improve kar sake",
        # we should probably loop. But let's stick to the single pass + Async Loop below.
        
        asyncio.run(autonomous_run(
            context="Personal AI system for decision making, automation, and business operations"
        ))
        exit(0)

    # ================= MANUAL MODE =================
    
    if MODE == "GOAL":
        # Check for pending goals but don't auto-resume unless asked (interactive placeholder)
        resume_pending_goals(auto=False) 
        
        from autonomy.goal_engine import run_goal_loop
        # Use TASK as the Goal Objective for now
        goal_result = run_goal_loop(TASK)
        
        if goal_result["status"] != "COMPLETED":
             exit(1)
             
    else:
        # SINGLE ATOMIC TASK MODE
        result = run_atomic_task(TASK)
        
        if not result["success"]:
            exit(1)

    print("\n================ END =================\n")
