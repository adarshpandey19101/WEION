
# test_memory_logic.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.memory_agent import decide_memory

def test_deterministic_gates():
    print("\n--- Test: Deterministic Gates ---")
    
    # CASE 1: Rejected & Low Score -> SKIP (No LLM call)
    print("1. Rejected + Low Score (0.2)...")
    verdict = {"accepted": False, "score": 0.2}
    execution_result = {"results": []}
    
    with patch("memory.memory_agent.ask_llm") as mock_llm:
        decision = decide_memory("Task", "Goal", execution_result, verdict)
        if decision["decision"] == "SKIP" and not mock_llm.called:
            print("✅ Correct: Skipped without LLM")
        else:
            print(f"❌ Failed: Decision={decision['decision']}, LLM Called={mock_llm.called}")

    # CASE 2: Accepted & Weak Score -> SKIP (No LLM call)
    print("2. Accepted + Weak Score (0.5)...")
    verdict = {"accepted": True, "score": 0.5}
    
    with patch("memory.memory_agent.ask_llm") as mock_llm:
        decision = decide_memory("Task", "Goal", execution_result, verdict)
        if decision["decision"] == "SKIP" and not mock_llm.called:
            print("✅ Correct: Skipped without LLM")
        else:
            print(f"❌ Failed: Decision={decision['decision']}, LLM Called={mock_llm.called}")

def test_llm_decision():
    print("\n--- Test: LLM Decision ---")
    
    # CASE 3: Accepted & High Score -> Call LLM
    print("3. Accepted + High Score (0.95)...")
    verdict = {"accepted": True, "score": 0.95}
    execution = {
        "results": [{"output": {"summary": "First principles is physics based reasoning."}}]
    }
    
    fake_llm_response = """
    ```json
    {
        "decision": "STORE",
        "memory_type": "knowledge",
        "summary": "First principles thinking involves breaking problems down to fundamental truths.",
        "tags": ["thinking", "strategy"],
        "reason": "High quality definition."
    }
    ```
    """
    
    with patch("memory.memory_agent.ask_llm", return_value=fake_llm_response) as mock_llm:
        decision = decide_memory("Explain first principles", "Explain", execution, verdict)
        
        if decision["decision"] == "STORE" and decision["memory_type"] == "knowledge":
            print("✅ Correct: LLM decided to STORE")
        else:
            print(f"❌ Failed: Decision={decision}")

if __name__ == "__main__":
    test_deterministic_gates()
    test_llm_decision()
