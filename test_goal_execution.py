
# test_goal_execution.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from autonomy.goal_engine import run_goal_loop

def test_goal_loop():
    print("\n--- Test: Goal Execution Loop ---")
    
    # Mock Decomposition
    mock_decomposition = {
        "strategy_explanation": "Test Strategy",
        "tasks": ["Task 1", "Task 2"]
    }
    
    with patch("autonomy.goal_engine.decompose_goal", return_value=mock_decomposition) as mock_decomp:
        
        # Mock Atomic Task Runner
        # Task 1: Success
        # Task 2: Success
        def mock_run_task(task):
            print(f"[Mock] Running {task}")
            return {"success": True, "verdict": {"accepted": True, "score": 1.0}}
            
        with patch("autonomy.goal_engine.run_atomic_task", side_effect=mock_run_task) as mock_runner:
            
            result = run_goal_loop("Build a rocket")
            
            print("\nGoal Result:")
            print(result)
            
            if result["status"] == "COMPLETED" and result["progress"] == "2/2":
                print("\n✅ SUCCESS: Goal completed all tasks.")
            else:
                print(f"\n❌ FAILURE: Unexpected status {result['status']}")

if __name__ == "__main__":
    test_goal_loop()
