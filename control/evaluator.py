
import logging
import yaml
import os
from typing import Dict, Any, List
from api.schema import PlannerOutput

# Initialize logger
logger = logging.getLogger(__name__)

# Load Rules
RULES_PATH = os.path.join(os.path.dirname(__file__), "rules.yaml")
try:
    with open(RULES_PATH, "r") as f:
        RULES = yaml.safe_load(f)
except Exception as e:
    logger.error(f"Failed to load validation rules: {e}")
    RULES = {}

def load_rules():
    """Reloads rules from YAML (useful for tuning)"""
    global RULES
    try:
        with open(RULES_PATH, "r") as f:
            RULES = yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to reload rules: {e}")

def verify(plan: PlannerOutput, execution_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministically evaluates the execution of a plan.
    Returns: { "accepted": bool, "score": float, "issues": List[str] }
    """
    issues = []
    score = 1.0
    
    # 1. Check Execution Success
    if not execution_result.get("success", False):
        issues.append("execution_failed")
        score = 0.0
        return {
            "accepted": False,
            "score": score,
            "issues": issues
        }

    results = execution_result.get("results", [])
    
    # 2. Check Completeness (Did all steps run?)
    executed_step_ids = {r.get("step_id") for r in results}
    planned_step_ids = {s.step_id for s in plan.steps}
    
    missing_steps = planned_step_ids - executed_step_ids
    if missing_steps:
        issues.append(f"missing_steps_{list(missing_steps)}")
        score -= (0.2 * len(missing_steps))

    # 3. Check Structure & Rules per Step
    for result in results:
        action = result.get("action")
        output = result.get("output", {})
        
        # Get rules for this action
        action_rules = RULES.get(action, {})
        
        # Check Required Fields
        required_fields = action_rules.get("required_fields", [])
        for field in required_fields:
            if field not in output:
                issues.append(f"step_{result.get('step_id')}_missing_field_{field}")
                score -= 0.2
        
        # Check Min Length (if text content exists)
        min_len = action_rules.get("min_length", 0)
        # Check specific fields for length based on action type
        content_to_check = ""
        if action == "summarize":
            content_to_check = output.get("summary", "")
        elif action == "respond_user":
            content_to_check = output.get("message", "")
        elif action == "read_file":
            content_to_check = output.get("content", "")
            
        if content_to_check and len(content_to_check) < min_len:
            issues.append(f"step_{result.get('step_id')}_output_too_short")
            score -= 0.1

    # 4. Final Threshold Check
    threshold = RULES.get("general", {}).get("confidence_threshold", 0.6)
    
    # Ensure score doesn't go below 0
    score = max(0.0, score)
    
    accepted = score >= threshold and "execution_failed" not in issues
    
    # If partial execution is not allowed
    allow_partial = RULES.get("general", {}).get("allow_partial", False)
    if not allow_partial and missing_steps:
        accepted = False

    return {
        "accepted": accepted,
        "score": round(score, 2),
        "issues": issues
    }
