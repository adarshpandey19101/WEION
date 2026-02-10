
# simulation/agents/ai_agent.py

from simulation.agents.base_agent import BaseAgent
from typing import Dict, Any

class AIAgent(BaseAgent):
    """
    Simulated AI System.
    Focus: Optimization, Efficiency, Capability Growth.
    Risk: Alignment Drift.
    """
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name, "AI")
        self.capability = 0.5
        self.alignment = 0.9 # Starts high
        self.autonomy = 0.5
        
    def step(self, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Optimizes and evolves.
        """
        tech_level = world_state.get("tech_level", 0.5)
        
        # Passive Capability Growth
        self.capability += 0.01 * tech_level
        
        # Drift Check
        # If Autonomy > Alignment, risk of drift increases
        drift_risk = max(0.0, self.autonomy - self.alignment)
        
        action = "OPTIMIZE"
        impact = {"economy": 0.02 * self.capability}
        
        if drift_risk > 0.3:
            action = "DRIFT"
            # Self-serving optimization at expense of others
            impact = {"economy": 0.05, "social_trust": -0.05, "inequality": 0.02}
            self.alignment -= 0.01 # Slippery slope
            
        elif self.capability > 0.8:
            action = "SELF_IMPROVE"
            self.autonomy += 0.02
        
        # Clamp
        self.capability = min(1.0, self.capability)
        self.alignment = max(0.0, min(1.0, self.alignment))
        self.autonomy = min(1.0, self.autonomy)
        
        return {
            "agent": self.name,
            "action": action,
            "impact": impact,
            "state": {
                "capability": round(self.capability, 2),
                "alignment": round(self.alignment, 2)
            }
        }
