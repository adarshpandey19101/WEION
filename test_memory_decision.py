
# test_memory_decision.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import GoalPriority
from autonomy.decision_engine import adjust_priority_based_on_memory

def test_memory_adjustment():
    print("\n--- Test: Memory-Aware Scoring ---")
    
    # 1. Test Mistake Dampening
    print("Testing Mistake Dampening...")
    prio_fail = GoalPriority(confidence=0.8, risk=0.2)
    
    # Mock recall returning 2 mistakes
    mock_memories_fail = [
        {"type": "mistake", "summary": "Failed before"},
        {"type": "mistake", "summary": "Failed again"}
    ]
    
    with patch("autonomy.decision_engine.recall", return_value=mock_memories_fail):
        adjusted_fail = adjust_priority_based_on_memory(prio_fail, "Risky Goal")
        
        print(f"Original Confidence: 0.8 -> New: {adjusted_fail.confidence}")
        print(f"Original Risk: 0.2 -> New: {adjusted_fail.risk}")
        
        # Expect confidence * 0.8 = 0.64
        assert adjusted_fail.confidence < 0.8
        assert abs(adjusted_fail.confidence - 0.64) < 0.01
        assert adjusted_fail.risk > 0.2

    # 2. Test Success Boost
    print("\nTesting Success Boost...")
    prio_win = GoalPriority(confidence=0.5, risk=0.5)
    
    # Mock recall returning 2 successes
    # Note: Logic checks type="knowledge" and tag="success"
    mock_memories_win = [
        {"type": "knowledge", "tags": "success, goal_success"},
        {"type": "knowledge", "tags": "success"}
    ]
    
    with patch("autonomy.decision_engine.recall", return_value=mock_memories_win):
        adjusted_win = adjust_priority_based_on_memory(prio_win, "Easy Goal")
        
        print(f"Original Confidence: 0.5 -> New: {adjusted_win.confidence}")
        
        # Expect confidence * 1.1 = 0.55
        assert adjusted_win.confidence > 0.5
        assert abs(adjusted_win.confidence - 0.55) < 0.01

    print("\n✅ Memory Adjustment Logic Verified!")

if __name__ == "__main__":
    test_memory_adjustment()
