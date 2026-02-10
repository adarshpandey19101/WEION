
# autonomy/collective_memory.py

import json
import os
from typing import Dict, Any, List

COLLECTIVE_MEMORY_PATH = "logs/civilization_memory.json"

class CollectiveMemory:
    """
    Phase 33: Collective Memory Pool 🧠
    "No owner. No ego. Only truth."
    
    Stores anonymized outcomes of strategies.
    Example: {"Strategy_Aggressive_Sales": {"success": 40, "fail": 10}}
    """
    
    _memory = {}
    
    @classmethod
    def load(cls):
        if not os.path.exists(COLLECTIVE_MEMORY_PATH):
            cls._memory = {}
            return
            
        try:
            with open(COLLECTIVE_MEMORY_PATH, 'r') as f:
                cls._memory = json.load(f)
        except Exception:
            cls._memory = {}

    @classmethod
    def save(cls):
        os.makedirs("logs", exist_ok=True)
        with open(COLLECTIVE_MEMORY_PATH, 'w') as f:
            json.dump(cls._memory, f, indent=4)

    @classmethod
    def contribute(cls, strategy_name: str, success: bool):
        """
        Anonymized contribution.
        """
        cls.load()
        if strategy_name not in cls._memory:
            cls._memory[strategy_name] = {"success": 0, "fail": 0}
            
        if success:
            cls._memory[strategy_name]["success"] += 1
        else:
            cls._memory[strategy_name]["fail"] += 1
            
        cls.save()

    @classmethod
    def get_consensus(cls, strategy_name: str) -> str:
        """
        Returns the civilization's verdict on a strategy.
        """
        cls.load()
        data = cls._memory.get(strategy_name)
        if not data:
            return "UNKNOWN"
            
        total = data["success"] + data["fail"]
        if total < 5:
            return "INSUFFICIENT_DATA"
            
        rate = data["success"] / total
        
        if rate > 0.8:
            return "HIGHLY_EFFECTIVE"
        elif rate > 0.5:
            return "MODERATE"
        else:
            return "POOR"
