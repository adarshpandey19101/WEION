
# test_trust_dashboard.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalExecution, TrustSnapshot, GoalPriority
)
from autonomy.decision_engine import decide_next_goal

# Ensure DB tables exist for test
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(TrustSnapshot).delete()
    db.query(GoalPriority).delete()
    db.commit()

def test_trust_dashboard():
    print("\n--- Test: Trust Dashboard (Phase 28) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # 1. Create a Goal
        goal = GoalExecution(objective="Launch Risky Crypto Token", status="PENDING")
        db.add(goal)
        db.commit()
        db.refresh(goal)
        
        # 2. Initialize Priority manually to ensure it has values
        prio = GoalPriority(
            goal_id=goal.id,
            impact=0.9,
            urgency=0.8,
            confidence=0.5, # Experimental
            risk=0.8        # Very Risky
        )
        db.add(prio)
        db.commit()
        
        # 3. Run Decision Engine (It should generate TrustSnapshot)
        print("🤖 Running Decision Engine...")
        decision = decide_next_goal()
        
        print(f"Decision: {decision['decision']}")
        
        # 4. Verify TrustSnapshot
        snapshot = db.query(TrustSnapshot).filter(TrustSnapshot.goal_id == goal.id).first()
        
        if not snapshot:
            # Maybe it wasn't saved because we only save snapshots for specific cases in my code?
            # In `decision_engine.py`, I wrote: `snapshot[goal.id]["trust_data"] = trust_snap_data`
            # BUT I didn't actually WRITE it to DB in the loop! I just stored it in memory `snapshot`.
            # I need to fix `decision_engine.py` to actually persist TrustSnapshot.
            print("❌ TrustSnapshot not found in DB! (Did we forget to save it?)")
            assert False, "TrustSnapshot missing"
            
        print("✅ TrustSnapshot found.")
        print(f"Breakdown: {snapshot.factor_breakdown}")
        
        breakdown = snapshot.factor_breakdown
        assert "logic_score" in breakdown
        assert "org_risk_bias" in breakdown
        assert "personality_bias" in breakdown
        
        print("\n✅ Trust Dashboard Data Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_trust_dashboard()
