
# test_enterprise_constitution.py
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalExecution, DecisionLog, ResponsibilityChain, UserOrganization, GoalPriority
)
from autonomy.decision_engine import decide_next_goal
from autonomy.explainability_engine import generate_board_report
from autonomy.constitution_loader import Constitution

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(DecisionLog).delete()
    db.query(ResponsibilityChain).delete()
    db.query(UserOrganization).delete()
    db.query(GoalPriority).delete()
    db.commit()

def test_enterprise_stack():
    print("\n--- Test: Enterprise Constitutional AI (Phase 32) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # 1. Setup Data
        # Goal
        goal = GoalExecution(objective="Increase Q3 Revenue", status="PENDING", org_id=1)
        db.add(goal)
        db.commit()
        
        # Users
        u_owner = UserOrganization(user_id="user_owner", org_id=1, role="OWNER")
        u_member = UserOrganization(user_id="user_member", org_id=1, role="MEMBER")
        db.add_all([u_owner, u_member])
        db.commit()
        
        # 2. Test Constitution Loading
        print("\n🔍 Verifying Constitution...")
        const = Constitution.load()
        assert const["core_principles"][0]["id"] == "no_data_exfiltration"
        print("✅ Constitution Loaded.")
        
        # 3. Test Sandbox (MEMBER should be BLOCKED)
        print("\n🧱 Testing Sandbox (MEMBER Role)...")
        block_decision = decide_next_goal(user_id="user_member", org_id=1)
        print(f"Member Decision: {block_decision['decision']} - {block_decision['reason']}")
        
        assert block_decision["decision"] == "BLOCKED"
        assert "Insufficient Role Permissions" in block_decision["reason"]
        print("✅ Member successfully blocked from Execution.")
        
        # 4. Test Authorized Action (OWNER) & Liability Tracking
        print("\n🔓 Testing Authorized Action (OWNER Role)...")
        # Ensure goal priority exists
        prio = GoalPriority(goal_id=goal.id, confidence=0.8, impact=0.9, score=0.9)
        db.add(prio)
        db.commit()
        
        action_decision = decide_next_goal(user_id="user_owner", org_id=1)
        print(f"Owner Decision: {action_decision['decision']}")
        
        assert action_decision["decision"] == "SELECT"
        assert action_decision["goal_id"] == goal.id
        
        # Check Responsibility Chain
        chain = db.query(ResponsibilityChain).filter(
            ResponsibilityChain.goal_id == goal.id
        ).first()
        
        assert chain is not None
        print(f"✅ Responsibility Chain Logged: DecisionID={chain.decision_id} | ApprovedBy={chain.who_approved}")
        assert chain.who_approved == "WEION_CEO_ENGINE"
        
        # 5. Test Board Report Generation
        print("\n📊 Testing Board Report...")
        report = generate_board_report(
            decision_id=str(chain.decision_id),
            action=f"Select Goal {goal.id}",
            risk_score=chain.risk_score or 0.1,
            roi_estimate=15.5,
            alternatives=["Goal 2 (Rejected)", "Goal 3 (Paused)"]
        )
        print(report)
        assert "EXECUTIVE BOARD REPORT" in report
        assert "ROI Impact: +15.5%" in report
        print("✅ Board Report Generated.")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_enterprise_stack()
