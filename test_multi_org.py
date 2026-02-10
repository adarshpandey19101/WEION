
# test_multi_org.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalExecution, TrustSnapshot, GoalPriority, Organization, UserOrganization
)
from autonomy.decision_engine import decide_next_goal

# Ensure DB tables exist for test
Base.metadata.drop_all(bind=engine) # Force schema update
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(TrustSnapshot).delete()
    db.query(GoalPriority).delete()
    db.query(Organization).delete()
    db.commit()

def test_multi_org_brain():
    print("\n--- Test: Multi-Org Cognitive Brain (Phase 29) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # 1. Create Organizations
        bank = Organization(name="Iron Bank", industry="BANKING", risk_profile=0.1)
        startup = Organization(name="Y-Combinator Startup", industry="STARTUP", risk_profile=0.9)
        db.add(bank)
        db.add(startup)
        db.commit()
        db.refresh(bank)
        db.refresh(startup)
        
        print(f"Created Orgs: {bank.name} (Risk Tol: {bank.risk_profile}), {startup.name} (Risk Tol: {startup.risk_profile})")
        
        # 2. Create Same Risky Goal for Both
        # Goal A (Bank)
        goal_bank = GoalExecution(org_id=bank.id, objective="Launch High Risk DeFi Protocol", status="PENDING")
        db.add(goal_bank)
        
        # Goal B (Startup)
        goal_startup = GoalExecution(org_id=startup.id, objective="Launch High Risk DeFi Protocol", status="PENDING")
        db.add(goal_startup)
        
        db.commit()
        
        # 3. Initialize Priorities (Identical Risk = 0.8)
        p1 = GoalPriority(goal_id=goal_bank.id, impact=0.8, risk=0.8, confidence=0.5, org_id=bank.id)
        p2 = GoalPriority(goal_id=goal_startup.id, impact=0.8, risk=0.8, confidence=0.5, org_id=startup.id)
        db.add(p1)
        db.add(p2)
        db.commit()
        
        # 4. Run Decision Engine for BANK
        print("\n🏦 Running Bank Decision...")
        decision_bank = decide_next_goal(org_id=bank.id)
        
        snap_bank = db.query(TrustSnapshot).filter(TrustSnapshot.goal_id == goal_bank.id).first()
        score_bank = snap_bank.final_score
        print(f"Bank Score: {score_bank:.3f}")
        print(f"Bank Breakdown: {snap_bank.factor_breakdown}")
        
        # 5. Run Decision Engine for STARTUP
        print("\n🚀 Running Startup Decision...")
        decision_startup = decide_next_goal(org_id=startup.id)
        
        snap_startup = db.query(TrustSnapshot).filter(TrustSnapshot.goal_id == goal_startup.id).first()
        score_startup = snap_startup.final_score
        print(f"Startup Score: {score_startup:.3f}")
        print(f"Startup Breakdown: {snap_startup.factor_breakdown}")
        
        # 6. Assertions
        assert score_startup > score_bank, f"Startup score ({score_startup}) should be higher than Bank ({score_bank})"
        
        # Check Isolation
        # decision_bank should NOT include startup goals
        # (Implicitly checked by filter logic in engine, result should be goal_bank or None)
        assert decision_bank.get("goal_id") == goal_bank.id or decision_bank.get("decision") == "NONE"
        
        print("\n✅ Multi-Org Brain Verified! Different minds for different orgs.")

    finally:
        db.close()

if __name__ == "__main__":
    test_multi_org_brain()
