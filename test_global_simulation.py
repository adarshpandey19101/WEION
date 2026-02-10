
# test_global_simulation.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.world_model import WorldState, SimulationEngine
from simulation.scenario_runner import ScenarioRunner

def test_simulation_stack():
    print("\n--- Test: Global Simulation & Co-Governance (Phase 35) ---")
    
    # 1. Test World Model & Engine
    print("\n🌍 Testing World Model Projection...")
    initial_world = WorldState(economy=0.5, social_trust=0.5, inequality=0.2)
    
    # Scenario: Automation (Should increase inequality)
    result = SimulationEngine.run_simulation(initial_world, "Automate Hiring", duration=5)
    
    final_state = result["final_state"]
    print(f"Initial Inequality: 0.2 -> Final: {final_state['inequality']}")
    assert final_state["inequality"] > 0.2
    print("✅ Logic Verified: Automation increased inequality.")
    
    # 2. Test Scenario Runner (Monte Carlo)
    print("\n🎲 Testing Scenario Runner (Monte Carlo)...")
    
    # Scenario A: High Risk (Automation)
    # Simulation engine logic adds +0.08 inequality per step for "automate"
    # 5 steps = +0.40. 0.2 + 0.4 = 0.6. Not catastrophic (0.8 threshold).
    # Wait, simple model logic:
    # if "automate" ... inequality += 0.08.
    # Loop duration=10 in ScenarioRunner run.
    # 10 * 0.08 = 0.8. Initial 0.2 + 0.8 = 1.0. 
    # 1.0 > 0.8 -> EXTREME_INEQUALITY -> Catastrophic.
    
    risk_report = ScenarioRunner.analyze_decision_risk("Automate Hiring", runs=10)
    print(f"Risk Report for 'Automate Hiring':")
    print(f"- Catastrophic Prob: {risk_report['catastrophic_probability']}")
    print(f"- Recommendation: {risk_report['recommendation']}")
    
    assert risk_report['catastrophic_probability'] > 0.05
    assert risk_report['recommendation'] == "BLOCKED_BY_SIMULATION"
    print("✅ High Risk Decision Blocked.")
    
    # Scenario B: Low Risk (Safe Action)
    risk_report_safe = ScenarioRunner.analyze_decision_risk("Optimize Database", runs=10)
    print(f"\nRisk Report for 'Optimize Database':")
    print(f"- Recommendation: {risk_report_safe['recommendation']}")
    
    assert risk_report_safe['recommendation'] == "PROCEED"
    print("✅ Safe Decision Allowed.")

if __name__ == "__main__":
    test_simulation_stack()
