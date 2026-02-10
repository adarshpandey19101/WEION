
# simulation/dynamics/collapse_dynamics.py

from typing import Dict, Any

class CollapseDynamics:
    """
    Simulates Systemic Failure Points.
    "How does it end?"
    """
    
    @classmethod
    def check_risk(cls, world_state: Dict[str, float]) -> Dict[str, Any]:
        """
        Calculates collapse probability and type.
        """
        trust = world_state.get("social_trust", 0.5)
        inequality = world_state.get("inequality", 0.0)
        economy = world_state.get("economy", 0.5)
        
        prob = 0.0
        reasons = []
        
        # 1. Social Collapse (Anarchy)
        if trust < 0.1:
            prob = max(prob, 0.9)
            reasons.append("SOCIAL_CONTRACT_FAILURE")
        elif trust < 0.2:
            prob = max(prob, 0.4)
            reasons.append("LOW_TRUST_INSTABILITY")
            
        # 2. Economic Collapse (Revolution)
        if inequality > 0.9:
            prob = max(prob, 0.8)
            reasons.append("REVOLUTION_RISK")
            
        # 3. Stagnation (Decay)
        if economy < 0.1:
            prob = max(prob, 0.6)
            reasons.append("ECONOMIC_COLLAPSE")
            
        return {
            "collapse_probability": round(prob, 2),
            "reasons": reasons,
            "status": "CRITICAL" if prob > 0.7 else "STABLE" if prob < 0.2 else "WARNING"
        }
