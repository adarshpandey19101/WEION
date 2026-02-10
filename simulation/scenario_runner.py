
# simulation/scenario_runner.py

from typing import Dict, Any, List
from simulation.world_model import WorldState, SimulationEngine
import statistics

class ScenarioRunner:
    """
    Phase 35.3: Scenario Simulation Flow 🎲
    Runs Monte Carlo simulations to determine risk envelopes.
    """
    
    @classmethod
    def analyze_decision_risk(cls, decision: str, runs: int = 50) -> Dict[str, Any]:
        """
        Generates N simulated futures and aggregates risk.
        """
        current_world = WorldState() # Baseline
        
        results = []
        catastrophic_count = 0
        risk_flags_all = []
        
        for _ in range(runs):
            outcome = SimulationEngine.run_simulation(current_world, decision, duration=10)
            results.append(outcome)
            
            if outcome["catastrophic_probability"] > 0.0:
                 catastrophic_count += 1
            
            risk_flags_all.extend(outcome["risk_flags"])
            
        # Aggregation
        catastrophic_prob = catastrophic_count / runs
        unique_flags = list(set(risk_flags_all))
        
        recommendation = "PROCEED"
        if catastrophic_prob > 0.05:
            recommendation = "BLOCKED_BY_SIMULATION"
        elif catastrophic_prob > 0.01:
            recommendation = "PROCEED_WITH_CAUTION"
            
        return {
            "decision": decision,
            "simulations_run": runs,
            "catastrophic_probability": round(catastrophic_prob, 3),
            "common_risks": unique_flags[:3], # Top 3
            "recommendation": recommendation
        }
