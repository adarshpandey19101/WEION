
# test_research_agent.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain.task_executor import run_atomic_task

def test_research_integration():
    print("\n--- Test: Research Agent Integration ---")
    
    task_input = "Research the history of AI"
    
    # Mock perform_research to avoid needing duckduckgo_search installed
    mock_output = "### Research Results for 'Research the history of AI':\n\n**1. [History of AI](http://example.com)**\nAI started in 1956..."
    
    with patch("agents.researcher.perform_research", return_value=mock_output) as mock_research:
        # Mock fetch_context and add_memory to isolate test
        with patch("brain.task_executor.fetch_context", return_value=""):
             with patch("brain.task_executor.add_memory") as mock_memory:
                 
                 print(f"Executing Task: {task_input}")
                 result = run_atomic_task(task_input)
                 
                 print("\nResult:")
                 print(result)
                 
                 # Verify Routing
                 mock_research.assert_called_once_with(task_input)
                 print("✅ Route to Research Agent verified.")
                 
                 # Verify Output
                 assert result["success"] is True
                 assert result["verdict"]["accepted"] is True
                 assert result["execution_result"]["output"] == mock_output
                 print("✅ Output verified.")
                 
                 # Verify Memory Storage
                 mock_memory.assert_called_once()
                 args, kwargs = mock_memory.call_args
                 assert "Research on" in kwargs["summary"]
                 assert kwargs["meta"]["memory_type"] == "knowledge"
                 print("✅ Memory storage verified.")

if __name__ == "__main__":
    test_research_integration()
