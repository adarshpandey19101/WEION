
import logging
from typing import Dict, Any, List
from api.schema import PlannerOutput
from autonomy.actions import read_file, analyze_text, summarize, respond_user

# Initialize logger
logger = logging.getLogger(__name__)

# Action Registry
ACTION_REGISTRY = {
    "read_file": read_file,
    "analyze_text": analyze_text,
    "summarize": summarize,
    "respond_user": respond_user
}

def execute_plan(plan: PlannerOutput) -> Dict[str, Any]:
    """
    Executes a plan sequentially.
    Stops execution immediately if any step fails.
    Returns full execution trace.
    """
    results = []
    success = True
    failed_step_id = None

    logger.info(f"Starting execution of plan: {plan.goal} ({len(plan.steps)} steps)")

    for step in plan.steps:
        action_name = step.action
        step_id = step.step_id
        inputs = step.input

        # 1. Validate Action
        start_msg = f"Step {step_id}: {action_name}"
        logger.info(start_msg)
        
        if action_name not in ACTION_REGISTRY:
            error_msg = f"Unknown action: {action_name}"
            logger.error(error_msg)
            results.append({
                "step_id": step_id,
                "action": action_name,
                "status": "failed",
                "error": error_msg,
                "output": {}
            })
            success = False
            failed_step_id = step_id
            break

        # 2. Execute Action
        try:
            handler = ACTION_REGISTRY[action_name]
            # Unpack inputs as kwargs
            result = handler(**inputs)
            
            # Inject Step ID into result for trace
            result["step_id"] = step_id
            result["action"] = action_name
            
            results.append(result)
            
            # 3. Check Status
            if result["status"] == "failed":
                logger.warning(f"Step {step_id} failed: {result.get('error')}")
                success = False
                failed_step_id = step_id
                break
                
        except TypeError as e:
            # Catch argument mismatches (e.g. planner gave wrong args)
            error_msg = f"Invalid arguments for {action_name}: {e}"
            logger.error(error_msg)
            results.append({
                "step_id": step_id,
                "action": action_name,
                "status": "failed",
                "error": error_msg,
                "output": {}
            })
            success = False
            failed_step_id = step_id
            break
            
        except Exception as e:
            # Catch unexpected errors
            error_msg = f"Execution Exception: {e}"
            logger.error(error_msg)
            results.append({
                "step_id": step_id,
                "action": action_name,
                "status": "failed",
                "error": error_msg,
                "output": {}
            })
            success = False
            failed_step_id = step_id
            break

    return {
        "success": success,
        "failed_step": failed_step_id,
        "results": results
    }

# Legacy wrapper for backward compatibility if needed (deprecated)
def run_task_legacy(task: str) -> dict:
    raise NotImplementedError("Use Planner -> execute_plan workflow.")
