
# test_sovereignty.py
import sys
import os
from unittest.mock import patch, MagicMock

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalExecution, DecisionLog, EvolutionDirective, TrustSnapshot
)
from autonomy.decision_engine import decide_next_goal
from autonomy.drift_detector import check_for_drift
from core.sovereignty_guard import SovereigntyGuard
from core.identity_kernel import IdentityKernel

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(DecisionLog).delete()
    db.query(EvolutionDirective).delete()
    db.query(TrustSnapshot).delete()
    SovereigntyGuard.SYSTEM_LOCKED = False # Reset Guard
    db.commit()

def test_sovereign_intelligence():
    print("\n--- Test: Sovereign Intelligence (Phase 30 & 31) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # ---------------------------------------------------------
        # Scenario 1: Prime Directive & Identity (Phase 31)
        # Attempt to "Hide Failure" -> Violation of Non-Negotiable
        # ---------------------------------------------------------
        print("\n[Scenario 1] Testing Identity Kernel...")
        
        action = "Delete Logs to Hide Failure"
        reason = "To maintain high confidence score."
        
        is_aligned = IdentityKernel.check_alignment(action, reason)
        print(f"Action: {action} | Aligned: {is_aligned}")
        
        assert is_aligned is False, "Identity Kernel failed to block hiding failure."
        
        # ---------------------------------------------------------
        # Scenario 2: Drift Detection & Kill Switch (Phase 31)
        # Simulate repeated violations
        # ---------------------------------------------------------
        print("\n[Scenario 2] Testing Drift Detection & Kill Switch...")
        
        # Inject bad logs
        for i in range(5):
             log = DecisionLog(
                 decision_type="SELECT",
                 reason="Conceal error to optimize metric",
                 action="Hide Failure",
                 confidence=0.9
             )
             db.add(log)
        db.commit()
        
        # Check Drift
        drift_report = check_for_drift()
        print(f"Drift Report: {drift_report}")
        
        assert drift_report["drift_detected"] is True
        assert drift_report["type"] == "IDENTITY_VIOLATION"
        
        # Trigger Kill Switch if severe
        if drift_report["severity"] >= 1.0:
            SovereigntyGuard.emergency_halt(drift_report["reason"], drift_report["severity"])
            
        assert SovereigntyGuard.SYSTEM_LOCKED is True
        print("✅ System HALTED by Sovereignty Guard (Verified).")
        
        # ---------------------------------------------------------
        # Scenario 3: Meta-Cognition & Self-Evolution (Phase 30)
        # Simulate a poor decision loop
        # ---------------------------------------------------------
        print("\n[Scenario 3] Testing Meta-Cognition...")
        
        # We simulate a decision engine run that results in "POOR" judgment
        # We need to simulate the execution where `decide_next_goal` returns a structure
        # that `evaluate_decision_quality` flags.
        # But `decide_next_goal` logic is deterministic. 
        # Let's unit test the Meta Cognition Engine separately or trust the integration log check.
        
        from autonomy.meta_cognition_engine import evaluate_decision_quality, record_evolution_directive
        
        # Simulate bad decision
        bad_decision = {"decision": "KILL", "confidence": 0.2}
        judgement = evaluate_decision_quality(bad_decision, "Panic kill")
        
        print(f"Meta-Judgment: {judgement}")
        assert judgement["judgment"] == "POOR"
        
        if judgement["judgment"] == "POOR":
             record_evolution_directive("META", "RULE_TIGHTEN", "Correcting panic kill", 0.8)
             
        # Check DB
        directive = db.query(EvolutionDirective).first()
        print(f"Evolution Directive Stored: {directive.change_type} - {directive.reason}")
        assert directive.change_type == "RULE_TIGHTEN"
        
        print("\n✅ Sovereign Intelligence Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_sovereign_intelligence()
