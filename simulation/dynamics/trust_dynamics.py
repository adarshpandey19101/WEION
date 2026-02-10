
# simulation/dynamics/trust_dynamics.py

from typing import Dict, Any

class TrustDynamics:
    """
    Simulates Social Trust Capital.
    "Trust arrives on foot and leaves on horseback."
    """
    
    @classmethod
    def update(cls, world_state: Dict[str, float]) -> Dict[str, float]:
        """
        Updates social trust based on world state.
        """
        trust = world_state.get("social_trust", 0.5)
        inequality = world_state.get("inequality", 0.0)
        economy = world_state.get("economy", 0.5)
        
        delta = 0.0
        
        # 1. Inequality Erosion
        if inequality > 0.5:
            delta -= (inequality - 0.5) * 0.1
            
        # 2. Economic Stability Boost
        if economy > 0.6:
            delta += 0.01
        elif economy < 0.3:
            delta -= 0.05
            
        # 3. Collapse Spiral (Self-Reinforcing)
        if trust < 0.2:
            delta -= 0.05 # Panic accelerates distrust
            
        new_trust = max(0.0, min(1.0, trust + delta))
        
        return {
            "social_trust": round(new_trust, 2),
            "trust_delta": round(delta, 3)
        }
