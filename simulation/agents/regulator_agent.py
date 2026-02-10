
# simulation/agents/regulator_agent.py

from simulation.agents.base_agent import BaseAgent
from typing import Dict, Any

class RegulatorAgent(BaseAgent):
    """
    Simulated Government / Regulator.
    Focus: Stability, Equality, Fairness.
    Characteristic: Reacts with lag.
    """
    def __init__(self, agent_id: str):
        super().__init__(agent_id, "Government", "REGULATOR")
        self.strictness = 0.5
        self.bureaucracy = 0.5
        self.lag_counter = 0
        
    def step(self, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Intervenes if things get out of hand.
        """
        inequality = world_state.get("inequality", 0.0)
        monopoly_risk = world_state.get("monopoly_risk", 0.0) # Calculated by Dynamics
        
        action = "MONITOR"
        impact = {}
        
        # Lag simulation: Only act every 3 steps or if crisis
        self.lag_counter += 1
        
        if self.lag_counter >= 3:
            self.lag_counter = 0
            
            if inequality > 0.7:
                 action = "TAX_RICH"
                 impact = {"inequality": -0.05, "economy": -0.01}
            
            elif monopoly_risk > 0.6:
                 action = "ANTITRUST"
                 impact = {"monopoly_risk": -0.1, "economy": -0.02}
                 
            elif world_state.get("social_trust", 1.0) < 0.3:
                 action = "STABILIZE"
                 impact = {"social_trust": 0.05, "freedom": -0.05}

        return {
            "agent": self.name,
            "action": action,
            "impact": impact,
            "state": {
                "strictness": round(self.strictness, 2)
            }
        }
