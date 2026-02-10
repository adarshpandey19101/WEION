
# simulation/agents/org_agent.py

from simulation.agents.base_agent import BaseAgent
from typing import Dict, Any

class OrgAgent(BaseAgent):
    """
    Simulated Corporation / Organization.
    Focus: Profit, Growth, Market Share.
    """
    def __init__(self, agent_id: str, name: str):
        super().__init__(agent_id, name, "ORG")
        self.capital = 0.5
        self.market_share = 0.1
        self.risk_tolerance = 0.6
        
    def step(self, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Maximizes growth.
        """
        economy = world_state.get("economy", 0.5)
        regulation = world_state.get("regulation_level", 0.5)
        
        action = "MAINTAIN"
        impact = {}
        
        # High Economy -> Invest
        if economy > 0.6:
            action = "EXPAND"
            self.market_share += 0.02
            impact = {"economy": 0.01, "inequality": 0.01}
            
        # Low Regulation -> Power Grab
        if regulation < 0.3:
            action = "BUILD_MONOPOLY"
            self.market_share += 0.05
            impact = {"inequality": 0.05, "social_trust": -0.02}
            
        # Clamp
        self.market_share = max(0.0, min(1.0, self.market_share))
        
        return {
            "agent": self.name,
            "action": action,
            "impact": impact,
            "state": {
                "market_share": round(self.market_share, 2),
                "capital": round(self.capital, 2)
            }
        }
