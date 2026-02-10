
# simulation/dynamics/inequality_dynamics.py

from typing import Dict, Any, List

class InequalityDynamics:
    """
    Simulates Wealth Gap & Resource Accumulation.
    "The rich get richer, unless..."
    """
    
    @classmethod
    def update(cls, agents: List[Any], world_state: Dict[str, float]) -> Dict[str, float]:
        """
        Updates agent resources based on capital accumulation logic.
        """
        inequality = world_state.get("inequality", 0.0)
        economy = world_state.get("economy", 0.5)
        
        # 1. Capital Accumulation (Compound Growth)
        # Agents with > 0.5 resources grow faster
        for agent in agents:
            if agent.type == "ORG" or agent.type == "AI":
                growth_rate = 0.01 * economy
                if agent.resources > 0.5:
                    growth_rate *= 1.5 # Wealth Advantage
                
                agent.resources += growth_rate
                
            # Humans lose resources if inequality is high (Cost of Living)
            if agent.type == "HUMAN" and inequality > 0.6:
                agent.resources -= 0.01

            # Clamp
            agent.resources = max(0.0, min(1.0, agent.resources))
            
        # 2. Recalculate Inequality Metric (Simple Variance)
        resources = [a.resources for a in agents]
        if not resources: return {"inequality": 0.0}
        
        avg_res = sum(resources) / len(resources)
        variance = sum([(r - avg_res)**2 for r in resources]) / len(resources)
        new_inequality = min(1.0, variance * 4) # Scale factor
        
        return {
            "inequality": round(new_inequality, 2)
        }
