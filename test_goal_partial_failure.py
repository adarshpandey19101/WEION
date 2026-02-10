
# test_goal_partial_failure.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autonomy.goal_engine import run_goal_loop

def test_goal_partial_failure():
    print("\n--- Test: Goal Partial Failure ---")
    
    # Mock Decomposition
    mock_decomposition = {
        "strategy_explanation": "Test Strategy",
        "tasks": ["Task A (Succeeds)", "Task B (Fails)", "Task C (Should Skip)"]
    }
    
    with patch("autonomy.goal_engine.decompose_goal", return_value=mock_decomposition) as mock_decomp:
        
        # Mock Atomic Task Runner
        def mock_run_task(task, extra_context=None):
            if extra_context:
                print(f"[Mock] Extra Context Received: {extra_context}")
                
            if "Succeeds" in task:
                print(f"[Mock] Running {task} -> SUCCESS")
                return {"success": True, "verdict": {"accepted": True, "score": 1.0}}
            elif "Fails" in task:
                print(f"[Mock] Running {task} -> FAILURE")
                return {"success": False, "verdict": {"accepted": False, "score": 0.0, "issues": ["execution_failed"]}}
            else:
                print(f"[Mock] Running {task} -> SHOULD NOT RUN")
                return {"success": True, "verdict": {"accepted": True, "score": 1.0}}
            
        with patch("autonomy.goal_engine.run_atomic_task", side_effect=mock_run_task) as mock_runner:
            
            # We also need to patch add_memory to verify it's called
            with patch("autonomy.goal_engine.add_memory") as mock_memory:
                
                result = run_goal_loop("Build a rocket")
                
                print("\nGoal Result:")
                print(result)
                
                # Verification
                if result["status"] == "FAILED":
                    print("✅ Status is FAILED as expected.")
                else:
                    print(f"❌ FAILURE: Status is {result['status']}")

                # Progress should be 1/3 (Task A success, Task B fail, Task C skip)
                if result["progress"] == "1/3": 
                     print(f"✅ Progress captured correctly: {result['progress']}")
                else:
                     print(f"❌ FAILURE: Unexpected progress {result['progress']}")
                
                # Verify Memory Call
                failed_call = False
                for call in mock_memory.call_args_list:
                    if call.kwargs.get("meta", {}).get("memory_type") == "mistake":
                        failed_call = True
                        print("✅ Mistake memory stored (Exact enum match).")
                
                if not failed_call:
                    print("❌ FAILURE: Mistake memory not stored.")
                    
                # Verify that Task C was NOT run
                # We check the print output or mock calls
                # call_args_list of mock_runner
                calls = [c[0][0] for c in mock_runner.call_args_list]
                if "Task C (Should Skip)" in calls:
                    print("❌ FAILURE: Stopped-after-failure rule broken. Task C ran.")
                else:
                    print("✅ STRICT STOP: Task C did not run.")

if __name__ == "__main__":
    test_goal_partial_failure()
