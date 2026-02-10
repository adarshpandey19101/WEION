
# simulation/agents/human_agent.py

from simulation.agents.base_agent import BaseAgent
from typing import Dict, Any

class HumanAgent(BaseAgent):
    """
    Simulated Human Population Actor.
    Focus: Well-being, Freedom, Trust.
    """
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "Public", "HUMAN")
        self.happiness = 0.8
        self.freedom = 0.8
        self.trust = 0.8
        
    def step(self, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Reacts to the world state.
        """
        # 1. Update Internal State based on World
        # Inequality hurts happiness
        if world_state["inequality"] > 0.6:
            self.happiness -= 0.05
            
        # Low trust hurts stability
        if world_state["social_trust"] < 0.4:
            self.trust -= 0.1
            
        # 2. Decide Action
        action = "ADAPT"
        impact = {}
        
        # Panic Threshold
        if self.trust < 0.2:
            action = "PANIC"
            impact = {"social_trust": -0.1, "economy": -0.05}
            
        # Protest Threshold
        elif self.happiness < 0.3:
            action = "PROTEST"
            impact = {"economy": -0.02, "social_trust": -0.05}
            
        # Clamp stats
        self.happiness = max(0.0, min(1.0, self.happiness))
        self.trust = max(0.0, min(1.0, self.trust))
        
        return {
            "agent": self.name,
            "action": action,
            "impact": impact,
            "state": {
                "happiness": round(self.happiness, 2),
                "trust": round(self.trust, 2)
            }
        }
