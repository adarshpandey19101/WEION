
# autonomy/constitution_loader.py

import yaml
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

CONSTITUTION_PATH = "autonomy/enterprise_constitution.yaml"

class Constitution:
    _data = {}
    
    @classmethod
    def load(cls):
        if cls._data:
            return cls._data
            
        if not os.path.exists(CONSTITUTION_PATH):
            logger.error(f"Constitution not found at {CONSTITUTION_PATH}")
            return {}
            
        try:
            with open(CONSTITUTION_PATH, 'r') as f:
                cls._data = yaml.safe_load(f)
            logger.info("📜 Enterprise Constitution Loaded.")
        except Exception as e:
            logger.critical(f"Failed to load Constitution: {e}")
            raise RuntimeError("System Halt: Constitution Corrupted")
            
        return cls._data

    @classmethod
    def get_risk_boundary(cls, key: str) -> Any:
        cls.load()
        return cls._data.get("risk_boundaries", {}).get(key)
        
    @classmethod
    def get_authority_power(cls, role: str) -> str:
        cls.load()
        return cls._data.get("authority_hierarchy", {}).get(role.upper(), {}).get("power", "NONE")
