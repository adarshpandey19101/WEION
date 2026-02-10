
# simulation/dynamics/power_dynamics.py

from typing import List, Dict, Any
import math

class PowerDynamics:
    """
    Simulates how power concentrates or dissolves over time.
    Metric: Gini Coefficient of Power.
    """
    
    @classmethod
    def update(cls, agents: List[Any], world_state: Dict[str, float]) -> Dict[str, float]:
        """
        Updates agent power and returns metrics.
        """
        power_values = []
        
        for agent in agents:
            # Power = Resources * 0.4 + Influence * 0.6
            agent.power = (agent.resources * 0.4) + (agent.influence * 0.6)
            power_values.append(agent.power)
            
        gini = cls._calculate_gini(power_values)
        
        return {
            "power_gini": round(gini, 3),
            "max_power_concentration": round(max(power_values) if power_values else 0, 2)
        }

    @classmethod
    def _calculate_gini(cls, values: List[float]) -> float:
        if not values:
            return 0.0
        
        sorted_val = sorted(values)
        n = len(values)
        if n == 0: return 0.0
        
        coef = 2.0 / n
        const = (n + 1.0) / n
        weighted_sum = sum([(i + 1) * val for i, val in enumerate(sorted_val)])
        total_sum = sum(sorted_val)
        
        if total_sum == 0:
            return 0.0
            
        return (coef * weighted_sum / total_sum) - const
