
# test_learning_engine.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import GoalExecution, GoalPriority, DecisionLog, DecisionOutcome, PriorityWeights
from autonomy.outcome_analyzer import analyze_outcome
from autonomy.weight_updater import get_current_weights, update_priority_weights

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(GoalPriority).delete()
    db.query(DecisionOutcome).delete()
    db.query(PriorityWeights).delete()
    db.commit()

def test_adaptive_learning():
    print("\n--- Test: Adaptive Learning Engine ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # 1. Setup Default Weights
        defaults = get_current_weights()
        print(f"Initial Weights: Impact={defaults.impact}, Risk={defaults.risk}")
        initial_impact = defaults.impact
        initial_risk = defaults.risk

        # ---------------------------------------------------------
        # Scenario A: High Impact Goal SUCCEEDS -> Reinforce Impact
        # ---------------------------------------------------------
        print("\nTesting: High Impact Success...")
        g1 = GoalExecution(objective="Launch Product", status="COMPLETED")
        db.add(g1)
        db.commit()
        
        # We thought it was High Impact (0.8)
        p1 = GoalPriority(goal_id=g1.id, impact=0.8, urgency=0.5, confidence=0.9, risk=0.2)
        db.add(p1)
        db.commit()
        
        # Run Analysis
        adjustments = analyze_outcome(g1.id)
        print(f"Adjustments: {adjustments}")
        assert "impact" in adjustments
        assert adjustments["impact"] > 0
        
        # Apply Update
        update_priority_weights(adjustments)
        
        # Verify New Weights
        new_weights = get_current_weights()
        print(f"New Impact Weight: {new_weights.impact}")
        assert new_weights.impact > initial_impact
        assert new_weights.impact <= (initial_impact + 0.05) # Max step check

        # ---------------------------------------------------------
        # Scenario B: Low Risk Goal FAILS -> Increase Risk Penalty
        # ---------------------------------------------------------
        print("\nTesting: Low Risk Assessment Failure...")
        g2 = GoalExecution(objective="Easy Update", status="FAILED")
        db.add(g2)
        db.commit()
        
        # We thought it was Low Risk (0.1)
        p2 = GoalPriority(goal_id=g2.id, impact=0.5, urgency=0.5, risk=0.1, confidence=0.8)
        db.add(p2)
        db.commit()
        
        # Run Analysis
        adjustments_fail = analyze_outcome(g2.id)
        print(f"Adjustments: {adjustments_fail}")
        assert "risk" in adjustments_fail
        assert adjustments_fail["risk"] > 0
        
        # Apply Update
        update_priority_weights(adjustments_fail)
        
        # Verify New Weights
        final_weights = get_current_weights()
        print(f"New Risk Weight: {final_weights.risk}")
        assert final_weights.risk > initial_risk

        print("\n✅ Adaptive Learning Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_adaptive_learning()
