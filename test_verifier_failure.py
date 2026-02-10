
# test_verifier_failure.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from control.evaluator import verify
from api.schema import PlannerOutput, PlannerStep

def test_execution_failure():
    print("\n--- Test: Execution Failure ---")
    plan = PlannerOutput(
        goal="Read file",
        confidence=1.0,
        steps=[PlannerStep(step_id=1, action="read_file", input={"path": "bad.txt"})]
    )
    
    # Simulate Actioner reporting failure
    execution_result = {
        "success": False,
        "failed_step": 1,
        "results": [
            {"step_id": 1, "action": "read_file", "status": "failed", "error": "File not found"}
        ]
    }
    
    verdict = verify(plan, execution_result)
    print(verdict)
    
    if not verdict["accepted"] and verdict["score"] == 0.0 and "execution_failed" in verdict["issues"]:
        print("✅ Correctly REJECTED due to execution failure")
    else:
        print("❌ Failed checking execution failure")

def test_missing_fields():
    print("\n--- Test: Missing Fields ---")
    plan = PlannerOutput(
        goal="Analyze text",
        confidence=1.0,
        steps=[PlannerStep(step_id=1, action="analyze_text", input={"text": "some text"})]
    )
    
    # Simulate Actioner success but missing 'risks' field
    execution_result = {
        "success": True,
        "results": [
            {
                "step_id": 1, 
                "action": "analyze_text", 
                "status": "success", 
                "output": {
                    "key_points": ["A"], 
                    "themes": ["B"]
                    # MISSING 'risks'
                }
            }
        ]
    }
    
    verdict = verify(plan, execution_result)
    print(verdict)
    
    # Score should be < 1.0 (penalty -0.2)
    # Threshold is 0.6. Score start 1.0 -> 0.8. Should be ACCEPTED but with ISSUES.
    if verdict["score"] < 1.0 and any("missing_field_risks" in i for i in verdict["issues"]):
        print("✅ Correctly identified missing field")
    else:
        print("❌ Failed checking missing fields")

if __name__ == "__main__":
    test_execution_failure()
    test_missing_fields()
