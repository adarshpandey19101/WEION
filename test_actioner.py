
# test_actioner.py
import sys
import os
import asyncio
from typing import List

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.schema import PlannerOutput, PlannerStep
from autonomy.task_runner import execute_plan
from autonomy.actions import read_file, _validate_path

def test_path_validation():
    print("\n--- Testing Path Validation ---")
    
    safe_paths = ["uploads/test.txt", "data/db.sqlite", "/Users/adarshkumarpandey21/Desktop/personal-ai/uploads/file.txt"]
    unsafe_paths = ["../secret.txt", "/etc/passwd", "frontend/src/App.tsx", "backend/config.py"]
    
    for p in safe_paths:
        is_safe = _validate_path(p)
        print(f"Path: {p} -> Safe? {is_safe} [{'✅' if is_safe else '❌'}]")
        
    for p in unsafe_paths:
        is_safe = _validate_path(p)
        print(f"Path: {p} -> Safe? {is_safe} [{'✅' if not is_safe else '❌'}]")

def test_execution_flow():
    print("\n--- Testing Execution Flow ---")
    
    # Mock Plan: Read unsafe file -> Should FAIL and STOP
    mock_plan = PlannerOutput(
        goal="Test Failure",
        confidence=1.0,
        steps=[
            PlannerStep(step_id=1, action="respond_user", input={"message": "Starting..."}),
            PlannerStep(step_id=2, action="read_file", input={"path": "../outside.txt"}),
            PlannerStep(step_id=3, action="respond_user", input={"message": "Should not reach here"})
        ]
    )
    
    result = execute_plan(mock_plan)
    
    print(f"Success: {result['success']}")
    print(f"Failed Step: {result['failed_step']}")
    print(f"Results Count: {len(result['results'])}")
    
    executed_steps = [r['step_id'] for r in result['results']]
    print(f"Executed Steps: {executed_steps}")
    
    if result['success'] == False and result['failed_step'] == 2 and 3 not in executed_steps:
        print("✅ Correctly stopped on failure")
    else:
        print("❌ Failed to stop or unexpected result")

if __name__ == "__main__":
    test_path_validation()
    test_execution_flow()
