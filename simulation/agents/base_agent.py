
# simulation/agents/base_agent.py

from typing import Dict, Any

class BaseAgent:
    """
    Base Class for Simulated Actors in the Civilization Sandbox.
    """
    def __init__(self, agent_id: str, name: str, agent_type: str):
        self.id = agent_id
        self.name = name
        self.type = agent_type
        
        # Core stats (0.0 to 1.0)
        self.power = 0.1
        self.resources = 0.1
        self.influence = 0.1
        
        # State
        self.active = True
    
    def step(self, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Executes one simulation step.
        Returns proposed actions or state changes.
        """
        raise NotImplementedError("Subclasses must implement step()")
    
    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "power": round(self.power, 2),
            "resources": round(self.resources, 2),
            "influence": round(self.influence, 2)
        }
