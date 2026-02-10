
import logging
from typing import List, Dict, Any
from datetime import datetime
from api.database import SessionLocal
from api.models import GoalExecution, AtomicTaskCheckpoint
from autonomy.task_decomposer import decompose_goal
from brain.task_executor import run_atomic_task
from memory.vector_store import add_memory

# Initialize logger
logger = logging.getLogger(__name__)

class GoalState:
    def __init__(self, objective: str, context: str = "", resume_from_db: GoalExecution = None):
        if resume_from_db:
            self.objective = resume_from_db.objective
            self.context = resume_from_db.context
            self.status = resume_from_db.status
            self.tasks = resume_from_db.tasks or []
            self.current_task_index = resume_from_db.current_task_index
            self.results = resume_from_db.results or []
            self.completed_count = len([r for r in self.results if r.get("verdict", {}).get("accepted", False)]) if self.results else 0
            self.error = resume_from_db.error
            self.db_id = resume_from_db.id
        else:
            self.objective = objective
            self.context = context
            self.status = "PENDING"
            self.tasks: List[str] = []
            self.current_task_index = 0
            self.results: List[Dict] = []
            self.completed_count = 0
            self.error = None
            self.db_id = None
        
        self.start_time = datetime.now()

    def to_dict(self):
        return {
            "objective": self.objective,
            "status": self.status,
            "progress": f"{self.completed_count}/{len(self.tasks)}",
            "current_task": self.tasks[self.current_task_index] if self.tasks and self.current_task_index < len(self.tasks) else None,
            "error": self.error,
            "results": self.results,
            "goal_id": self.db_id
        }

def run_goal_loop(objective: str, context: str = "", resume_goal_id: int = None) -> Dict[str, Any]:
    """
    Executes a high-level goal by decomposing it and running atomic tasks.
    Supports resuming from a DB ID.
    """
    print(f"\n🎯 STARTING GOAL: {objective} (Resume ID: {resume_goal_id})\n")
    
    db = SessionLocal()
    state = None
    
    try:
        # RESUME MODE or NEW MODE
        if resume_goal_id:
            goal_db = db.query(GoalExecution).filter(GoalExecution.id == resume_goal_id).first()
            if not goal_db:
                return {"error": f"Goal ID {resume_goal_id} not found", "status": "FAILED"}
            
            print(f"🔄 RESUMING GOAL ID {resume_goal_id}: {goal_db.objective}")
            print(f"   Status: {goal_db.status}, Progress: {goal_db.current_task_index}/{len(goal_db.tasks)}")
            
            state = GoalState(objective=goal_db.objective, context=goal_db.context, resume_from_db=goal_db)
            # Ensure status is RUNNING if it was PAUSED or crashed
            state.status = "RUNNING"
            goal_db.status = "RUNNING"
            db.commit()
            
        else:
            # NEW GOAL
            # 1. Create DB Record (Initial)
            goal_db = GoalExecution(
                objective=objective,
                context=context,
                status="RUNNING",
                tasks=[],
                results=[]
            )
            db.add(goal_db)
            db.commit()
            db.refresh(goal_db)
            
            state = GoalState(objective, context)
            state.db_id = goal_db.id

            # 2. Decompose
            try:
                decomposition = decompose_goal(objective, context)
                state.tasks = decomposition.get("tasks", [])
                print(f"Goal decomposed into {len(state.tasks)} tasks.")
                for i, t in enumerate(state.tasks):
                    print(f"  {i+1}. {t}")
                
                # Update DB with Tasks
                goal_db.tasks = state.tasks
                db.commit()
                
            except Exception as e:
                state.status = "FAILED"
                state.error = str(e)
                logger.error(f"Goal Decomposition Failed: {e}")
                
                goal_db.status = "FAILED"
                goal_db.error = str(e)
                db.commit()
                return state.to_dict()

            if not state.tasks:
                state.status = "FAILED"
                state.error = "No tasks generated"
                goal_db.status = "FAILED"
                goal_db.error = "No tasks generated"
                db.commit()
                return state.to_dict()

        # 3. Execution Loop
        total_tasks = len(state.tasks)
        
        # Determine start index (0 for new, saved index for resume)
        start_index = state.current_task_index
        
        for i in range(start_index, total_tasks):
            task_str = state.tasks[i]
            state.current_task_index = i
            
            # Update DB Progress before start
            goal_db.current_task_index = i
            db.commit()

            print(f"\n👉 EXECUTING TASK {i+1}/{total_tasks}: {task_str}")
            
            try:
                # Execute Atomic Task with Extra Context & Resume Flag
                extra_ctx = {
                    "goal": objective,
                    "goal_context": context,
                    "goal_id": state.db_id,
                    "resume": (resume_goal_id is not None)
                }
                
                result = run_atomic_task(task_str, extra_context=extra_ctx)
                state.results.append(result)
                
                # Check Verdict
                verdict = result.get("verdict", {})
                accepted = verdict.get("accepted", False)
                
                # --- PERSIST CHECKPOINT ---
                checkpoint = AtomicTaskCheckpoint(
                    goal_id=state.db_id,
                    task_index=i,
                    task_text=task_str,
                    verdict=verdict,
                    execution_result=result.get("execution_result", {})
                )
                db.add(checkpoint)
                
                # Update Goal Record
                goal_db.results = state.results
                db.commit()
                # --------------------------
                
                if accepted:
                    state.completed_count += 1
                    logger.info(f"Task {i+1} completed successfully.")
                else:
                    # Task Failed -> Strict Stop
                    state.status = "FAILED"
                    state.error = f"Task {i+1} failed: {verdict.get('issues', ['Unknown issues'])}"
                    print(f"\n❌ GOAL FAILED at Task {i+1}.")
                    
                    goal_db.status = "FAILED"
                    goal_db.error = state.error
                    db.commit()
                    
                    # Goal-Level Memory (Mistake)
                    issues = verdict.get("issues", [])
                    add_memory(
                        summary=(
                            f"FAILED GOAL: {objective}. "
                            f"Failure at task '{task_str}'. "
                            f"Issues: {issues}"
                        ),
                        meta={
                            "memory_type": "mistake",
                            "tags": ["goal_failure", "execution_error"],
                            "score": verdict.get("score", 0.0),
                            "source_task": objective
                        }
                    )
                    break # Stop Loop
                    
            except Exception as e:
                state.status = "FAILED"
                state.error = f"System Error at Task {i+1}: {e}"
                logger.error(f"Goal Loop Error: {e}")
                
                goal_db.status = "FAILED"
                goal_db.error = state.error
                db.commit()
                break

        # 4. Completion Check
        if state.completed_count == total_tasks:
            state.status = "COMPLETED"
            print(f"\n🏆 GOAL COMPLETED: {objective}")
            
            goal_db.status = "COMPLETED"
            db.commit()
            
            # Goal-Level Memory (Success)
            add_memory(
                summary=f"COMPLETED GOAL: {objective}. Executed {total_tasks} tasks.",
                meta={
                    "memory_type": "knowledge",
                    "tags": ["goal_success", "strategy"],
                    "score": 1.0,
                    "source_task": objective
                }
            )
        
        return state.to_dict()
        
    finally:
        db.close()
