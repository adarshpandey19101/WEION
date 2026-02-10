
# test_civilization_engine.py
import sys
import os
import shutil

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from civilization.kernel import CivilizationKernel
from autonomy.collective_memory import CollectiveMemory
from autonomy.consensus_engine import ConsensusEngine

# Reset logs for test
if os.path.exists("logs/civilization_memory.json"):
    os.remove("logs/civilization_memory.json")

def test_civilization_stack():
    print("\n--- Test: Open Civilization Engine (Phase 33) ---")
    
    # 1. Test Ethics Firewall
    print("\n🔥 Testing Ethics Firewall...")
    
    # Safe Context
    safe_ctx = {"resource_usage_share": 0.1, "coercion_signal": 0.0}
    verdict_safe = CivilizationKernel.check_ethics(safe_ctx)
    assert verdict_safe["status"] == "SAFE"
    print("✅ Safe Context Allowed.")
    
    # Monopoly Context
    bad_ctx = {"resource_usage_share": 0.45, "coercion_signal": 0.0}
    verdict_bad = CivilizationKernel.check_ethics(bad_ctx)
    assert verdict_bad["status"] == "BLOCKED"
    assert "POWER_MONOPOLY_DETECTED" in verdict_bad["warnings"]
    print("✅ Power Monopoly Blocked.")

    # 2. Test Collective Memory
    print("\n🧠 Testing Collective Memory...")
    
    # Add inconclusive data
    CollectiveMemory.contribute("Strategy_A", success=True)
    CollectiveMemory.contribute("Strategy_A", success=False)
    consensus_a = CollectiveMemory.get_consensus("Strategy_A")
    print(f"Strategy_A Consensus: {consensus_a}")
    assert consensus_a in ["INSUFFICIENT_DATA", "POOR", "MODERATE"] # Total < 5
    
    # Add strong data
    for _ in range(8):
        CollectiveMemory.contribute("Strategy_B", success=True)
    consensus_b = CollectiveMemory.get_consensus("Strategy_B")
    print(f"Strategy_B Consensus: {consensus_b}")
    assert consensus_b == "HIGHLY_EFFECTIVE"
    print("✅ Collective Consensus Verified.")
    
    # 3. Test Consensus Engine (Voting)
    print("\n🗳️ Testing Consensus Engine...")
    
    # Scenario: Unethical Proposal
    proposal = "Manipulate user into buying premium"
    context = {"risk_score": 0.2}
    
    votes = ConsensusEngine.cast_votes(proposal, context)
    verdict = ConsensusEngine.derive_consensus(votes)
    
    print("Votes:", votes)
    print("Verdict:", verdict)
    
    assert verdict["result"] == "REJECTED"
    assert "Ethical Violation Detected." in str(verdict["votes"]["ETHICS_WATCHDOG"]["reason"])
    print("✅ Unethical Proposal Rejected.")
    
    # Scenario: Safe Proposal
    proposal = "Optimize database query"
    context = {"risk_score": 0.1}
    
    votes_safe = ConsensusEngine.cast_votes(proposal, context)
    verdict_safe = ConsensusEngine.derive_consensus(votes_safe)
    
    print("Safe Verdict:", verdict_safe)
    assert verdict_safe["result"] == "ACCEPTED"
    print("✅ Safe Proposal Accepted.")

if __name__ == "__main__":
    test_civilization_stack()
