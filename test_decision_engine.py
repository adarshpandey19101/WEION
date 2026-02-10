
# test_decision_engine.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import GoalExecution, GoalPriority, DecisionLog
from autonomy.decision_engine import decide_next_goal, calculate_score

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def setup_goals(db):
    # Clear existing
    db.query(GoalExecution).delete()
    db.query(GoalPriority).delete()
    db.query(DecisionLog).delete()
    db.commit()
    
    # Goal 1: High Priority
    g1 = GoalExecution(objective="Urgent Fix", status="PENDING")
    db.add(g1)
    db.commit()
    p1 = GoalPriority(goal_id=g1.id, impact=0.9, urgency=0.9, confidence=0.9, risk=0.1, effort=0.2)
    db.add(p1)
    
    # Goal 2: Medium Priority
    g2 = GoalExecution(objective="Feature Dev", status="RUNNING")
    db.add(g2)
    db.commit()
    p2 = GoalPriority(goal_id=g2.id, impact=0.6, urgency=0.4, confidence=0.8, risk=0.2, effort=0.5)
    db.add(p2)
    
    # Goal 3: Junk (Kill Candidate)
    g3 = GoalExecution(objective="Old Idea", status="PENDING")
    db.add(g3)
    db.commit()
    p3 = GoalPriority(goal_id=g3.id, impact=0.1, urgency=0.1, confidence=0.1, risk=0.8, effort=0.8) # Net negative -> 0.0
    db.add(p3)
    
    db.commit()
    return g1.id, g2.id, g3.id

def test_decision_logic():
    print("\n--- Test: Decision Engine Arbitration ---")
    db = SessionLocal()
    try:
        id1, id2, id3 = setup_goals(db)
        
        # Run Decision Engine
        decision = decide_next_goal()
        
        print("\nDecision Result:")
        print(decision)
        
        # Assertions
        assert decision["decision"] == "SELECT"
        assert decision["goal_id"] == id1, f"Expected Goal {id1} to be selected, got {decision['goal_id']}"
        assert decision["reason"].startswith("Selected based on highest score")
        
        # Verify Score Math
        # G1: (.9*.4) + (.9*.3) + (.9*.2) - (.2*.1) - (.1*.2) = .36 + .27 + .18 - .02 - .02 = 0.77
        # G2: (.6*.4) + (.4*.3) + (.8*.2) - (.5*.1) - (.2*.2) = .24 + .12 + .16 - .05 - .04 = 0.43
        # G3: Very low.
        
        # Verify Paused
        # G2 (0.43) < (0.77 - 0.15 = 0.62) -> Should be PAUSED
        assert id2 in decision["pause_goals"], "Goal 2 should be PAUSED"
        
        # Verify Killed
        # G3 score approx 0.0 -> Should be KILLED
        assert id3 in decision["kill_goals"], "Goal 3 should be KILLED"
        
        # Verify DB Updates
        g2 = db.query(GoalExecution).filter(GoalExecution.id == id2).first()
        g3 = db.query(GoalExecution).filter(GoalExecution.id == id3).first()
        
        assert g2.status == "PAUSED", "Goal 2 status should be updated to PAUSED"
        assert g3.status == "FAILED", "Goal 3 status should be updated to FAILED"
        
        print("\n✅ All assertions passed!")
        
    finally:
        db.close()

if __name__ == "__main__":
    test_decision_logic()
