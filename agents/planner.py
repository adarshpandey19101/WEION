# agents/planner.py
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy.orm import Session
from brain.model import ask_llm
from api.database import SessionLocal
from api.models import PlannerLog
from api.schema import PlannerOutput, PlannerStep
from pydantic import ValidationError

# Initialize logger
logger = logging.getLogger(__name__)

ALLOWED_ACTIONS = {
    "read_file",
    "analyze_text",
    "summarize",
    "create_task",
    "store_memory",
    "respond_user"
}

PLANNER_SYSTEM_PROMPT = """
You are the WEION Planner Agent.
Your job is to decide WHAT actions are required to fulfill the user's request.
You must NOT answer the user directly unless you use the 'respond_user' action.

RULES:
1. Return ONLY valid JSON. No markdown formatting, no explanations, no text.
2. Use ONLY allowed actions: {allowed_actions}
3. If you are unsure, produce a 'respond_user' action instead of guessing.
4. Your output must match this schema exactly:
{{
  "goal": "string (The core objective)",
  "confidence": 0.0 to 1.0 (float),
  "steps": [
    {{
      "step_id": 1,
      "action": "allowed_action_name",
      "input": {{ "arg_name": "value" }}
    }}
  ]
}}

USER REQUEST: {task}
"""

def make_plan(task: str, context: Optional[str] = None) -> PlannerOutput:
    """
    Generates a structured plan for the given task.
    Enforces JSON schema and logs execution to DB.
    """
    db = SessionLocal()
    planner_log = PlannerLog(
        user_input=task,
        timestamp=datetime.now().isoformat(),
        planner_version="v1.0"
    )
    
    try:
        # Construct Prompt
        actions_list = ", ".join(sorted(ALLOWED_ACTIONS))
        prompt = PLANNER_SYSTEM_PROMPT.format(
            allowed_actions=actions_list,
            task=task
        )
        if context:
            prompt += f"\nCONTEXT: {context}"

        # LLM Call with Retries
        attempts = 0
        max_retries = 2
        raw_response = ""
        validated_plan = None
        error_reason = None

        while attempts <= max_retries:
            try:
                raw_response = ask_llm(prompt)
                
                # Clean generic markdown code blocks if present
                clean_json = raw_response.strip()
                if clean_json.startswith("```json"):
                    clean_json = clean_json[7:]
                if clean_json.endswith("```"):
                    clean_json = clean_json[:-3]
                clean_json = clean_json.strip()

                # Parse JSON
                parsed_data = json.loads(clean_json)
                
                # Pydantic Validation
                validated_plan = PlannerOutput(**parsed_data)
                
                # Logical Validation (Action Whitelist)
                for step in validated_plan.steps:
                    if step.action not in ALLOWED_ACTIONS:
                        raise ValueError(f"Action '{step.action}' is not allowed.")
                
                # Success
                planner_log.successful = True
                planner_log.parsed_plan = validated_plan.dict()
                planner_log.raw_output = raw_response
                planner_log.confidence = validated_plan.confidence
                break

            except (json.JSONDecodeError, ValidationError, ValueError) as e:
                attempts += 1
                error_reason = str(e)
                logger.warning(f"Planner validation failed (Request: {attempts}): {e}")
                if attempts <= max_retries:
                    prompt += f"\n\nERROR: Previous response was invalid JSON or violated schema. Fix this error: {e}"
        
        # Handling Failure after Retries
        if not validated_plan:
            planner_log.successful = False
            planner_log.raw_output = raw_response
            planner_log.error_reason = f"Max retries reached. Last error: {error_reason}"
            planner_log.confidence = 0.0
            
            # Safe Fallback
            validated_plan = PlannerOutput(
                goal="Clarify request with user due to planning failure",
                confidence=0.0,
                steps=[
                    PlannerStep(
                        step_id=1,
                        action="respond_user",
                        input={"message": "I'm having trouble understanding how to proceed. Could you rephrase your request?"}
                    )
                ]
            )

        db.add(planner_log)
        db.commit()
        return validated_plan

    except Exception as e:
        logger.error(f"Critical Planner Error: {e}")
        db.rollback()
        # Emergency Fallback
        return PlannerOutput(
            goal="System Error Fallback",
            confidence=0.0,
            steps=[
                PlannerStep(
                    step_id=1,
                    action="respond_user",
                    input={"message": "System error in Planner Agent."}
                )
            ]
        )
    finally:
        db.close()

def make_replan(task: str, context: Optional[str], failure_analysis: Dict[str, Any]) -> PlannerOutput:
    """
    Generates a corrected plan based on failure analysis.
    wraps make_plan but injects failure context.
    """
    failure_msg = f"""
    [PREVIOUS PLAN REJECTED]
    Failure Type: {failure_analysis.get('failure_type')}
    Root Causes: {failure_analysis.get('root_causes')}
    Recommended Fix: {failure_analysis.get('recommended_fix')}
    
    INSTRUCTION: Generate a NEW plan that implements these fixes.
    """
    
    full_context = f"{context}\n{failure_msg}" if context else failure_msg
    
    # Generate new plan
    new_plan = make_plan(task, context=full_context)
    
    # Penalize confidence for retry
    if new_plan:
        new_plan.confidence = max(0.0, new_plan.confidence - 0.15)
        
    return new_plan
