
# test_trust_narrative.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    GoalExecution, AuditLog, EmotionalMemory, DecisionLog
)
from autonomy.emotion_engine import detect_emotion, get_emotional_bias
from autonomy.narrative_engine import generate_decision_story
from autonomy.explainability_engine import generate_explanation

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(GoalExecution).delete()
    db.query(AuditLog).delete()
    db.query(EmotionalMemory).delete()
    db.commit()

def test_trust_narrative():
    print("\n--- Test: Trust, Emotion & Narrative (Phases 25-27) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # -------------------------------------------------------------
        # Phase 25: Trust & Explainability
        # -------------------------------------------------------------
        print("\n[Phase 25] Testing Explainability...")
        
        # Mock Decision Data
        goal = GoalExecution(objective="Launch Moonshot", status="PAUSED")
        db.add(goal)
        db.commit()
        
        scores = {
            "final_score": 0.25,
            "system_score": 0.2, # Low logic
            "user_score": 0.4
        }
        
        explanation = generate_explanation(
            decision="PAUSED",
            goal_objective=goal.objective,
            scores=scores,
            personality="CFO"
        )
        
        print(f"Explanation: {explanation['summary']}")
        print(f"Factors: {explanation['factors']}")
        
        assert "low overall priority" in explanation['summary']
        assert "System logic rated this low" in explanation['factors'][0]
        
        # Store Audit Log manually (simulating decision engine)
        audit = AuditLog(
            entity_type="GOAL",
            entity_id=goal.id,
            action="PAUSED",
            reason=explanation['summary'],
            scores_snapshot=scores
        )
        db.add(audit)
        db.commit()

        # -------------------------------------------------------------
        # Phase 26: Emotional Intelligence
        # -------------------------------------------------------------
        print("\n[Phase 26] Testing Emotion...")
        
        # User kills a goal -> Stress
        detect_emotion("user1", "GOAL_KILLED")
        
        mem = db.query(EmotionalMemory).first()
        print(f"Detected Emotion: {mem.emotion} (Trigger: {mem.trigger_event})")
        
        assert mem.emotion == "FRUSTRATED"
        
        bias = get_emotional_bias("FRUSTRATED")
        print(f"Bias for Frustrated: {bias}")
        assert bias < 0 # Frustration penalizes risk

        # -------------------------------------------------------------
        # Phase 27: Narrative Engine
        # -------------------------------------------------------------
        print("\n[Phase 27] Testing Storytelling...")
        
        story = generate_decision_story(goal.id)
        print("\n--- Story Output ---")
        print(story)
        print("--------------------")
        
        assert "Goal Story: Launch Moonshot" in story
        assert "Reasoning: Decided to PAUSED" in story # Grammar aside, it matches

        print("\n✅ Trust & Narrative Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_trust_narrative()
