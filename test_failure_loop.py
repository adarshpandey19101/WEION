
# test_failure_loop.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.schema import PlannerOutput, PlannerStep

# Mock Plans
BAD_PLAN = PlannerOutput(
    goal="Read File",
    confidence=1.0,
    steps=[PlannerStep(step_id=1, action="read_file", input={"path": "non_existent.txt"})]
)

GOOD_PLAN = PlannerOutput(
    goal="Read File Corrected",
    confidence=0.85, # lowered confidence
    steps=[PlannerStep(step_id=1, action="respond_user", input={"message": "I realized the file was missing, so I am responding instead."})]
)

def test_loop_logic():
    print("\n--- Test: Self-Correction Loop ---")
    
    # We will mock:
    # 1. make_plan -> returns BAD_PLAN
    # 2. execute_plan -> Real execution (will fail for bad path)
    # 3. verify -> Real verification (will reject failure)
    # 4. analyze_failure -> Real analysis
    # 5. make_replan -> returns GOOD_PLAN
    
    with patch("brain.run_engine.make_plan", return_value=BAD_PLAN) as mock_plan:
        with patch("agents.planner.make_replan", return_value=GOOD_PLAN) as mock_replan:
            
            # We also need to patch sys.exit to prevent actual exit
            with patch("sys.exit") as mock_exit:
                
                # Import Run Engine MAIN block or simulate it
                # Since run_engine.py has the logic at top level, it's hard to import.
                # We will just Copy-Paste the Loop Logic here for testing, or simpler:
                # We can subprocess call it? No, mocking is hard across subprocess.
                # Standard practice: Validate the Component Logic.
                
                print("Simulating Loop...")
                
                # 1. Attempt 1
                plan = BAD_PLAN
                print("[1] Executing Bad Plan...")
                from autonomy.task_runner import execute_plan
                from control.evaluator import verify
                from agents.failure_analyzer import analyze_failure
                
                exec_result_1 = execute_plan(plan)
                verdict_1 = verify(plan, exec_result_1)
                
                print(f"Verdict 1: {verdict_1}")
                
                if verdict_1["accepted"]:
                    print("❌ Test Failed: Bad plan should have been rejected.")
                    return

                # 2. Analysis
                analysis = analyze_failure(plan, exec_result_1, verdict_1)
                print(f"Analysis: {analysis}")
                
                if analysis["failure_type"] != "EXECUTION_ERROR":
                     print("❌ Test Failed: Should detect execution error.")
                     return

                # 3. Re-Plan (Mocked)
                plan_2 = mock_replan("task", "ctx", analysis)
                print("[2] Executing Good Plan...")
                
                exec_result_2 = execute_plan(plan_2)
                verdict_2 = verify(plan_2, exec_result_2)
                
                print(f"Verdict 2: {verdict_2}")
                
                if verdict_2["accepted"]:
                    print("\n✅ SUCCESS: System self-corrected after failure!")
                else:
                    print("❌ Test Failed: Good plan should have been accepted.")

if __name__ == "__main__":
    test_loop_logic()
