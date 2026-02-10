
# test_cognitive_os.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalPriority, UserPreference, UserBehaviorSignal, 
    GoalExecution, UserRole
)
from autonomy.preference_learner import learn_from_signal
from autonomy.arbitrator import calculate_role_score
from autonomy.personality import apply_personality_bias

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(UserPreference).delete()
    db.query(UserBehaviorSignal).delete()
    db.query(UserRole).delete()
    db.commit()

def test_cognitive_os():
    print("\n--- Test: Cognitive Operating System (Phases 19-21) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # -------------------------------------------------------------
        # Phase 19: Implicit Preference Learning
        # -------------------------------------------------------------
        print("\n[Phase 19] Testing Preference Learning...")
        user_id = "learner_user"
        
        # Default Preference
        pref = UserPreference(user_id=user_id, pref_risk_tolerance=0.5)
        db.add(pref)
        db.commit()
        
        # Signal: User KILLED a goal
        learn_from_signal(user_id, "GOAL_KILLED", goal_id=123)
        
        # Verify Risk Tolerance Dropped
        db.refresh(pref)
        print(f"Old Risk: 0.5 -> New Risk: {pref.pref_risk_tolerance:.2f}")
        assert pref.pref_risk_tolerance < 0.5
        assert abs(pref.pref_risk_tolerance - 0.45) < 0.01

        # -------------------------------------------------------------
        # Phase 20: Multi-User Arbitration
        # -------------------------------------------------------------
        print("\n[Phase 20] Testing Role Arbitration...")
        
        # Create Owner and Contributor
        r1 = UserRole(user_id="user_owner", role="OWNER")
        r2 = UserRole(user_id="user_intern", role="CONTRIBUTOR")
        db.add(r1)
        db.add(r2)
        db.commit()
        
        s1 = calculate_role_score("user_owner")
        s2 = calculate_role_score("user_intern")
        
        print(f"Owner Score: {s1}")
        print(f"Intern Score: {s2}")
        
        assert s1 == 1.0
        assert s2 == 0.3
        assert s1 > s2

        # -------------------------------------------------------------
        # Phase 21: Personality Intelligence
        # -------------------------------------------------------------
        print("\n[Phase 21] Testing Personality Bias...")
        
        # Goal: High Impact, Low Confidence
        prio = GoalPriority(
            impact=0.9, 
            urgency=0.2, 
            confidence=0.4, 
            risk=0.5
        )
        base_score = 0.5
        
        # CEO (Loves Impact)
        ceo_score = apply_personality_bias(base_score, prio, "CEO")
        print(f"CEO Score for High Impact: {ceo_score}")
        # Bonus: Impact(0.2) -> 0.7
        assert ceo_score > 0.6
        
        # Researcher (Loves Experimentation even if Low Confidence)
        res_score = apply_personality_bias(base_score, prio, "RESEARCHER")
        print(f"Researcher Score for Low Conf/High Impact: {res_score}")
        # Bonus: Exp(0.3) -> 0.8
        assert res_score > 0.6
        assert res_score > base_score

        print("\n✅ Cognitive OS Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_cognitive_os()
