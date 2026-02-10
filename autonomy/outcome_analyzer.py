
# autonomy/outcome_analyzer.py

import logging
from typing import Dict, Any, Optional
from api.database import SessionLocal
from api.models import GoalExecution, DecisionLog, DecisionOutcome, GoalPriority

# Initialize Logger
logger = logging.getLogger(__name__)

def analyze_outcome(goal_id: int) -> Dict[str, float]:
    """
    Analyzes a finished goal and recommends weight adjustments.
    Returns: Dict[str, float] (adjustments)
    """
    db = SessionLocal()
    adjustments = {}
    
    try:
        goal = db.query(GoalExecution).filter(GoalExecution.id == goal_id).first()
        if not goal:
            return {}
            
        # Get priority snapshot used for this goal? 
        # Or current priority record?
        # We need the GoalPriority associated with this goal to see what we THOUGHT it was.
        priority = db.query(GoalPriority).filter(GoalPriority.goal_id == goal_id).first()
        
        if not priority:
            return {}

        print(f"\n🧠 ANALYZING OUTCOME: {goal.objective} (Status: {goal.status})")
        
        # --- LOGIC RULES ---
        
        # 1. SUCCESS ANALYZER
        if goal.status == "COMPLETED":
            # If it was marked High Impact and Succeeded -> Good job, reinforce Impact
            if priority.impact > 0.7:
                adjustments["impact"] = 0.01  # Slight boost
                
            # If it was marked High Urgency and Succeeded -> Reinforce Urgency
            if priority.urgency > 0.7:
                adjustments["urgency"] = 0.01
                
            # If it was Low Effort and Succeeded -> Good, maybe lower effort weight? (Less penalty for effort)
            # Actually, if High Effort succeeded, maybe we promote effort capability?
            # Let's keep it simple.
            
            # Confidence check
            # If we were confident and succeeded -> Good calibration.
            if priority.confidence > 0.8:
                adjustments["confidence"] = 0.01

        # 2. FAILURE ANALYZER
        elif goal.status == "FAILED":
            # If High Risk goal Failed -> System was right to be wary, but maybe Risk weight should be higher to prevent running it?
            # Or if Low Risk goal Failed -> BAD ASSESSMENT. We underestimated Risk.
            
            if priority.risk < 0.4:
                # We thought it was safe, but it failed.
                print("   ⚠️ Low Risk Goal Failed. Increasing Risk Penalty.")
                adjustments["risk"] = 0.05  # Strong correction
            else:
                # We knew it was risky, and it failed.
                # Maybe increase risk weight to discourage running such things.
                adjustments["risk"] = 0.01

            # If High Confidence goal Failed -> Overconfident.
            if priority.confidence > 0.7:
                print("   ⚠️ High Confidence Goal Failed. Lowering Confidence Weight.")
                adjustments["confidence"] = -0.02 # Trust confidence less
                
        # Log outcome to DB
        outcome_entry = DecisionOutcome(
            goal_id=goal.id,
            outcome=goal.status,
            final_score=priority.score # approx
        )
        db.add(outcome_entry)
        db.commit()
        
        return adjustments

    except Exception as e:
        logger.error(f"Outcome Analysis Failed: {e}")
        return {}
    finally:
        db.close()
