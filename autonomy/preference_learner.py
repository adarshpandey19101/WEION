
# autonomy/preference_learner.py

import logging
from typing import Dict, Any
from api.database import SessionLocal
from api.models import UserPreference, UserBehaviorSignal, GoalExecution

logger = logging.getLogger(__name__)

# Constants for Learning Rate
LR_KILL_RISK = -0.05
LR_FAST_SPEED = 0.04
LR_RETRY_EXP = 0.03

def learn_from_signal(user_id: str, signal_type: str, goal_id: int = None, metadata: Dict = None):
    """
    Ingests a user behavior signal and updates preferences.
    """
    db = SessionLocal()
    try:
        # 1. Log Signal
        signal_entry = UserBehaviorSignal(
            user_id=user_id,
            signal_type=signal_type,
            goal_id=goal_id,
            signal_metadata=metadata or {}
        )
        db.add(signal_entry)
        db.commit()
        
        # 2. Get User Preference
        pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            pref = UserPreference(user_id=user_id)
            db.add(pref)
            db.commit()
            db.refresh(pref)
            
        print(f"\n🎭 LEARNING: Signal '{signal_type}' received for {user_id}...")
        
        updates_made = False
        
        # 3. Learning Logic (Deterministic V1)
        
        # RULE A: GOAL_KILLED
        # If user kills a goal, check if it was Risky. If so, they probably hate risk.
        if signal_type == "GOAL_KILLED" and goal_id:
            goal = db.query(GoalExecution).filter(GoalExecution.id == goal_id).first()
            # We assume we have risk info somewhere? 
            # Ideally we check the GoalPriority snapshot or re-assess.
            # For now, let's assume valid metadata or just general conservative drift.
            
            # Lower Risk Tolerance
            old_val = pref.pref_risk_tolerance
            new_val = max(0.0, min(1.0, old_val + LR_KILL_RISK))
            if old_val != new_val:
                pref.pref_risk_tolerance = new_val
                print(f"   📉 Adjustment: Risk Tolerance {old_val:.2f} -> {new_val:.2f}")
                updates_made = True

        # RULE B: GOAL_COMPLETED_FAST
        # User explicitly prioritized speed or marked it done quickly.
        elif signal_type == "GOAL_COMPLETED_FAST":
            old_val = pref.pref_speed_vs_quality
            new_val = max(0.0, min(1.0, old_val + LR_FAST_SPEED))
            if old_val != new_val:
                pref.pref_speed_vs_quality = new_val
                print(f"   📈 Adjustment: Speed Preference {old_val:.2f} -> {new_val:.2f}")
                updates_made = True

        # RULE C: GOAL_RETRIED
        # User keeps trying. High experimentation preference?
        elif signal_type == "GOAL_RETRIED":
            old_val = pref.pref_experimentation
            new_val = max(0.0, min(1.0, old_val + LR_RETRY_EXP))
            if old_val != new_val:
                pref.pref_experimentation = new_val
                print(f"   📈 Adjustment: Experimentation {old_val:.2f} -> {new_val:.2f}")
                updates_made = True
                
        if updates_made:
            db.commit()
            print("✅ User Preferences Updated.")
            
    except Exception as e:
        logger.error(f"Preference Learning Failed: {e}")
    finally:
        db.close()
