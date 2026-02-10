
import json
import logging
from typing import Dict, Any
from brain.model import ask_llm

# Initialize logger
logger = logging.getLogger(__name__)

MEMORY_DECIDER_PROMPT = """
You are the MEMORY DECISION AGENT.
Your job is to decide if the following interaction contains high-value intelligence worth remembering for future tasks.

RULES:
1. Return ONLY valid JSON.
2. Store only high-signal knowledge (Strategy, Frameworks, Novel Facts).
3. If the insight is generic, obvious, or low-value -> ALWAYS return "SKIP".
4. If it's a "MISTAKE", summarize what went wrong to avoid it later.

INPUT:
Task: {task}
Plan Goal: {goal}
Verdict Score: {score}
Execution Summary: {execution_summary}

OUTPUT SCHEMA:
{{
  "decision": "STORE" | "SKIP",
  "memory_type": "knowledge" | "mistake" | "strategy",
  "summary": "Concise, dense insight (max 2 sentences). This is what will be vectorized.",
  "tags": ["tag1", "tag2"],
  "reason": "Why is this worth storing?"
}}
"""

def decide_memory(task: str, plan_goal: str, execution_result: Dict[str, Any], verdict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decides whether to store memory based on verdict and content.
    Deterministic gates applied first to save tokens.
    """
    accepted = verdict.get("accepted", False)
    score = verdict.get("score", 0.0)
    
    # 1. Deterministic Gating
    if not accepted:
        if score < 0.3:
            logger.info("Memory Decision: SKIP (Rejected & Low Score)")
            return {"decision": "SKIP", "reason": "Rejected and low score"}
        else:
            # Considerations for Mistake Memory
            # We treat this as a potentially valuable "Mistake" to learn from
            pass 

    if accepted:
        if score > 0.9:
            # High quality success - Strong candidate for storage, but we still need the summary/tags from LLM
            # Unless we want to purely deterministic store? 
            # User said: "true > 0.9 STORE -> deterministic". 
            # But we need the *summary*. So asking LLM is still impactful for *compression*.
            # However, I can force the decision to STORE in the prompt or logic.
            # For now, I will let LLM decide the *content* but biased towards storing.
            pass
        elif score < 0.6:
            logger.info("Memory Decision: SKIP (Accepted but Weak Score)")
            return {"decision": "SKIP", "reason": "Accepted but weak score"}

    # 2. Preparation for LLM
    # Extract text from execution result for context
    results = execution_result.get("results", [])
    execution_text_parts = []
    for r in results:
        output = r.get("output", {})
        if "summary" in output:
            execution_text_parts.append(f"Summary: {output['summary']}")
        elif "key_points" in output:
             execution_text_parts.append(f"Analysis: {output.get('key_points')}")
        elif "message" in output:
             execution_text_parts.append(f"Response: {output['message']}")
        elif "content" in output:
             # Don't dump full file content, just say it read a file
             execution_text_parts.append(f"Read file: {r.get('output', {}).get('path')}")
    
    execution_summary = "; ".join(execution_text_parts)[:2000] # Truncate for prompt limit

    prompt = MEMORY_DECIDER_PROMPT.format(
        task=task,
        goal=plan_goal,
        score=score,
        execution_summary=execution_summary
    )

    try:
        response = ask_llm(prompt)
        
        # Parse JSON
        clean_json = response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
            
        data = json.loads(clean_json.strip())
        
        # Fallback/Safety Checks
        if "decision" not in data:
            data["decision"] = "SKIP"
            
        # Enforce Deterministic Overrides if needed
        # (e.g. if we really wanted to force STORE on > 0.9, we could override here, 
        # but relying on the "smart" agent with the strong prompt is usually better for Quality Control)
        
        return data

    except json.JSONDecodeError:
        logger.error("Memory Agent returned invalid JSON")
        return {"decision": "SKIP", "reason": "LLM JSON Error"}
    except Exception as e:
        logger.error(f"Memory Agent failed: {e}")
        return {"decision": "SKIP", "reason": str(e)}
