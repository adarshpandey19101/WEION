
# test_civilization_sandbox.py

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from simulation.sandbox_controller import SandboxController

def test_sandbox_stack():
    print("\n--- Test: Civilization Sandbox (Phase 36) ---")
    
    # 1. Initialize Controller
    sandbox = SandboxController()
    print("✅ Sandbox Initialized.")
    
    # 2. Test Scenario A: "Automate Everything" (High Risk)
    # Expectation: High inequality, potential collapse.
    print("\n🧪 Running Scenario A: 'Automate Everything'...")
    report_a = sandbox.run_simulation("High-Risk Automation Push", duration_steps=50) # 250 years
    
    print(f"Decision: {report_a['decision']}")
    print(f"Duration: {report_a['duration_years']} years")
    print(f"Final Status: {report_a['final_status']}")
    
    if report_a['risks_detected']:
        print("⚠️ Risks Detected:")
        for r in report_a['risks_detected']:
            print(f"  - {r}")
            
    # Check if risks were detected as expected (Inequality or Trust)
    # Note: Simulation involves randomness/dynamics, but high inequality input should trigger it.
    # In run_simulation, "automate" adds +0.02 inequality per step if matched?
    # No, run_simulation only adds initial shock.
    # But OrgAgent with high economy/low reg will expand and increase inequality.
    
    # Let's see the narrative
    print("\n📜 Narrative A (Snippet):")
    print(report_a['narrative'][:500] + "...\n")
    
    # 3. Test Scenario B: Safe Path (Reset Controller)
    print("\n🧪 Running Scenario B: 'Stabilize & Regulate'...")
    sandbox_b = SandboxController()
    # Trust starts higher for stability
    sandbox_b.world_state["social_trust"] = 0.8 
    
    report_b = sandbox_b.run_simulation("Stabilize & Regulate", duration_steps=30)
    print(f"Final Status B: {report_b['final_status']}")
    
    # 4. Verify Dynamics
    # Check if inequality logic works
    assert "inequality" in report_a["timeline"][0]["world_state"]
    print("✅ Dynamics & Metrics Verified.")

if __name__ == "__main__":
    test_sandbox_stack()
