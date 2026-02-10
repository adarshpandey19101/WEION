
# simulation/world_model.py

from typing import Dict, Any, List
import copy
import random

class WorldState:
    """
    Represents a compressed state of civilization.
    Signal > Detail.
    """
    def __init__(self, economy=0.5, social_trust=0.5, inequality=0.2, tech_level=0.5):
        self.economy = economy # 0.0 to 1.0 (Collapse to Utopia)
        self.social_trust = social_trust
        self.inequality = inequality
        self.tech_level = tech_level
        self.time_step = 0

    def to_dict(self):
        return {
            "economy": round(self.economy, 2),
            "social_trust": round(self.social_trust, 2),
            "inequality": round(self.inequality, 2),
            "tech_level": round(self.tech_level, 2)
        }

class SimulationEngine:
    """
    Phase 35: Global Simulation Engine 🌍
    "Reality, but consequence-safe."
    """
    
    @classmethod
    def run_simulation(cls, current_state: WorldState, decision: str, duration: int = 5) -> Dict[str, Any]:
        """
        Projects the world state forward by `duration` steps under `decision`.
        Returns the final state and risk profile.
        """
        sim_state = copy.deepcopy(current_state)
        history = []
        
        risk_flags = []
        
        for t in range(duration):
            sim_state.time_step += 1
            
            # --- SIMULATION LOGIC (Simplified Model) ---
            
            # Scenario: "Automate Hiring"
            if "automate" in decision.lower() and "hiring" in decision.lower():
                sim_state.economy += 0.05       # Efficiency Up
                sim_state.inequality += 0.08    # Inequality Up
                sim_state.social_trust -= 0.05  # Trust Down
                
            # Scenario: "Universal Basic Compute"
            elif "compute" in decision.lower() and "basic" in decision.lower():
                sim_state.tech_level += 0.1
                sim_state.inequality -= 0.05
                sim_state.economy -= 0.02 # Cost
                
            else:
                # Noise / Drift
                sim_state.economy += random.uniform(-0.01, 0.01)
            
            # -------------------------------------------
            
            # Bounds Check
            sim_state.economy = max(0.0, min(1.0, sim_state.economy))
            sim_state.social_trust = max(0.0, min(1.0, sim_state.social_trust))
            
            # Risk Detection
            if sim_state.inequality > 0.8:
                risk_flags.append("EXTREME_INEQUALITY")
            if sim_state.social_trust < 0.2:
                risk_flags.append("SOCIAL_COLLAPSE")
            
            history.append(sim_state.to_dict())
            
        return {
            "final_state": sim_state.to_dict(),
            "risk_flags": list(set(risk_flags)),
            "catastrophic_probability": len(risk_flags) * 0.2
        }
