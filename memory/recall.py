
# memory/recall.py

from typing import List, Dict
from memory.vector_store import recall
import logging

# Initialize logger
logger = logging.getLogger(__name__)

def fetch_context(task: str) -> str:
    """
    Retrieves context for the Planner.
    Fetches top memories, prioritizes them, and formats them as a string block.
    """
    try:
        memories = recall(task, k=5)
        
        if not memories:
            return ""

        # Prioritize: Strategy > Knowledge > Mistake -> Others
        # We can sort key based on type
        def type_priority(m):
            t = m.get("type", "").lower()
            if "strategy" in t: return 0
            if "knowledge" in t: return 1
            if "mistake" in t: return 2
            return 3
            
        memories.sort(key=type_priority)
        
        formatted_lines = ["PAST LEARNINGS:"]
        for m in memories:
            m_type = m.get("type", "INFO").upper()
            summary = m.get("summary", "")
            if summary:
                formatted_lines.append(f"- [{m_type}] {summary}")
                
        return "\n".join(formatted_lines)

    except Exception as e:
        logger.error(f"Recall failed: {e}")
        return ""
