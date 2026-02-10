
import asyncio
import logging
from typing import Dict, Any
from api.schema import PlannerOutput
from autonomy.task_runner import ACTION_REGISTRY

# Initialize logger
logger = logging.getLogger(__name__)

async def execute_plan_async(plan: PlannerOutput) -> Dict[str, Any]:
    """
    Async version of execute_plan.
    Wraps synchronous actions in asyncio.to_thread to prevent blocking event loop.
    """
    results = []
    success = True
    failed_step_id = None

    logger.info(f"Starting ASYNC execution of plan: {plan.goal}")

    for step in plan.steps:
        action_name = step.action
        step_id = step.step_id
        inputs = step.input

        if action_name not in ACTION_REGISTRY:
            error_msg = f"Unknown action: {action_name}"
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

        try:
            handler = ACTION_REGISTRY[action_name]
            
            # ⚡ Run sync action in thread pool
            result = await asyncio.to_thread(handler, **inputs)
            
            result["step_id"] = step_id
            result["action"] = action_name
            
            results.append(result)

            if result["status"] == "failed":
                success = False
                failed_step_id = step_id
                break

        except TypeError as e:
            error_msg = f"Invalid arguments for {action_name}: {e}"
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
            error_msg = f"Execution Exception: {e}"
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

async def run_task_async(task: str) -> Dict[str, Any]:
    """
    Legacy compatibility wrapper.
    Orchestrates Planner -> Actioner flow.
    """
    from agents.planner import make_plan
    
    # 1. Plan
    plan = make_plan(task)
    
    # 2. Execute
    result = await execute_plan_async(plan)
    
    return result
