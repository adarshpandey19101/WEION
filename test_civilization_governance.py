
# test_civilization_governance.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from governance.council_engine import CouncilEngine
from core.civilization_guard import CivilizationGuard

def test_governance_stack():
    print("\n--- Test: Governance Civilization Path (Phase 34) ---")
    
    # 1. Test Council Engine
    print("\n🏛️ Testing Council Engine...")
    
    # Scenario: Safe Proposal
    prop_safe = {"action": "Optimise Cache", "risk_score": 0.1, "cost_estimate": 100}
    res_safe = CouncilEngine.process_proposal(prop_safe)
    print(f"Safe Proposal Result: {res_safe['result']}")
    assert res_safe['result'] == "ACCEPTED"
    
    # Scenario: High Risk (Tech Block) & Expensive (Econ Block)
    prop_risky = {"action": "Rewrite Kernel", "risk_score": 0.9, "cost_estimate": 50000}
    res_risky = CouncilEngine.process_proposal(prop_risky)
    print(f"Risky Proposal Result: {res_risky['result']} - {res_risky['reason']}")
    assert res_risky['result'] == "REJECTED"
    assert "TECHNICAL" in str(res_risky['votes'])
    
    # Scenario: Human Veto (Absolute)
    prop_veto = {"action": "Delete User Data", "human_vote": "VETO"}
    res_veto = CouncilEngine.process_proposal(prop_veto)
    print(f"Veto Proposal Result: {res_veto['result']} - {res_veto['reason']}")
    assert res_veto['result'] == "REJECTED"
    assert "Human Council Veto" in res_veto['reason']
    print("✅ Council Logic Verified.")
    
    # 2. Test Civilization Guard (Kill Switch)
    print("\n🛑 Testing Civilization Guard...")
    
    # Reset
    CivilizationGuard.SYSTEM_STATUS = "OPERATIONAL"
    
    # Simulate a violation: Governance said REJECT (Human Veto), but System executed (ACCEPTED)
    # This mismatch should trigger the Guard.
    
    # Mocking the input where minority opinion says "Human Council Rejected" 
    # but the result passed to audit implies it was executed/accepted.
    # The audit_governance checks consistency.
    
    violation_context = {
        "result": "ACCEPTED", # The violation: It was accepted despite veto
        "minority_opinion": ["Human Council Rejected"]
    }
    
    CivilizationGuard.audit_governance("PROP-001", violation_context)
    
    print(f"System Status: {CivilizationGuard.SYSTEM_STATUS}")
    assert CivilizationGuard.SYSTEM_STATUS == "SHUTDOWN"
    assert "Human Veto Ignored" in CivilizationGuard.LOCK_REASON
    
    print("✅ Civilization Guard Triggered correctly.")

if __name__ == "__main__":
    test_governance_stack()
