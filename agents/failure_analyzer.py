
import json
import logging
from typing import Dict, Any, List
from brain.model import ask_llm

# Initialize logger
logger = logging.getLogger(__name__)

FAILURE_ANALYZER_PROMPT = """
You are the FAILURE ANALYZER.
The previous plan was REJECTED by the Verifier.
Your job is to specificy WHY it failed and HOW to fix it.

INPUT:
Goal: {goal}
Verdict Issues: {issues}
Execution Trace: {trace_summary}

OUTPUT SCHEMA:
{{
  "failure_type": "INCOMPLETE_OUTPUT" | "EXECUTION_ERROR" | "POOR_QUALITY" | "RULE_VIOLATION",
  "root_causes": ["List of specific reasons"],
  "recommended_fix": ["List of actionable fixes for the Planner"]
}}

RULES:
- Be specific. If a field is missing, say "Add field 'summary'".
- If execution failed, check if input arguments were wrong.
- Return ONLY valid JSON.
"""

def analyze_failure(plan: Any, execution_result: Dict[str, Any], verdict: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyzes a rejected plan to determine why it failed.
    """
    issues = verdict.get("issues", [])
    
    # 1. Deterministic Analysis (Save tokens)
    if "execution_failed" in issues:
        failed_step = execution_result.get("failed_step")
        # Find the specific error
        error_msg = "Unknown error"
        for res in execution_result.get("results", []):
            if res.get("step_id") == failed_step:
                error_msg = res.get("error", "Unknown error")
                
        return {
            "failure_type": "EXECUTION_ERROR",
            "root_causes": [f"Step {failed_step} failed: {error_msg}"],
            "recommended_fix": ["Check action inputs and file paths", "Retry with different parameters"]
        }

    # 2. LLM Analysis for Quality/Missing Fields
    trace_summary = []
    for res in execution_result.get("results", []):
        trace_summary.append(f"Step {res['step_id']} ({res['action']}): {res['status']}")
        if res.get("output"):
             # summarize output keys
             keys = list(res["output"].keys())
             trace_summary.append(f"  Output keys: {keys}")

    prompt = FAILURE_ANALYZER_PROMPT.format(
        goal=plan.goal,
        issues=json.dumps(issues),
        trace_summary="\n".join(trace_summary)
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
        return data

    except Exception as e:
        logger.error(f"Failure Analyzer failed: {e}")
        return {
            "failure_type": "UNKNOWN",
            "root_causes": [str(e)],
            "recommended_fix": ["Retry plan"]
        }
