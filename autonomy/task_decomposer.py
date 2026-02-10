
import json
import logging
from typing import List, Dict, Any
from brain.model import ask_llm

# Initialize logger
logger = logging.getLogger(__name__)

DECOMPOSER_PROMPT = """
You are the STRATEGIST (Task Decomposer).
Your job is to break down a HIGH-LEVEL GOAL into a sequence of ATOMIC, EXECUTABLE TASKS.

INPUT GOAL: {goal}
CONTEXT/CONSTRAINTS: {context}

RULES:
1. Return ONLY valid JSON.
2. Generate between 1 and 10 tasks.
3. Each task must be specific and actionable (e.g., "Research X", "Write code for Y", "Test Z").
4. AVOID vague verbs like "think", "understand", "explore", "consider". Use "analyze", "read", "verify" instead.
5. Each task description must be under 200 characters.

OUTPUT SCHEMA:
{{
  "strategy_explanation": "Brief reasoning...",
  "tasks": [
    "Task 1 description...",
    "Task 2 description..."
  ]
}}
"""

VAGUE_VERBS = ["think", "understand", "explore", "consider", "ponder", "imagine"]

def decompose_goal(goal: str, context: str = "") -> Dict[str, Any]:
    """
    Decomposes a goal into atomic tasks with deterministic validation.
    """
    prompt = DECOMPOSER_PROMPT.format(goal=goal, context=context)
    
    max_retries = 2
    attempts = 0
    
    while attempts <= max_retries:
        try:
            response = ask_llm(prompt)
            
            # Parse
            clean_json = response.strip()
            if clean_json.startswith("```json"):
                clean_json = clean_json[7:]
            if clean_json.endswith("```"):
                clean_json = clean_json[:-3]
            
            data = json.loads(clean_json.strip())
            tasks = data.get("tasks", [])
            
            # --- DETERMINISTIC VALIDATION ---
            
            # Rule 1: Task Count
            if not (1 <= len(tasks) <= 10):
                raise ValueError(f"Task count {len(tasks)} out of range (1-10).")
                
            # Rule 2: Logic Check per Task
            for i, task in enumerate(tasks):
                # Length check
                if len(task) > 200:
                    raise ValueError(f"Task {i+1} is too long (>200 chars).")
                
                # Vague verb check
                task_lower = task.lower()
                for verb in VAGUE_VERBS:
                    if verb in task_lower.split(): # simple word check
                         raise ValueError(f"Task {i+1} uses vague verb '{verb}'. Be more specific.")

            # Validation Passed
            logger.info(f"Goal decomposed into {len(tasks)} tasks.")
            return data

        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Decomposition validation failed (Attempt {attempts+1}): {e}")
            attempts += 1
            prompt += f"\n\nERROR: Previous output was invalid. {e}. Fix it."
            
    # Fallback if max retries reached
    logger.error("Decomposition failed after retries.")
    return {
        "strategy_explanation": "Fallback due to decomposition failure.",
        "tasks": [f"Analyze manually: {goal}"]  # Safe fallback
    }
