
# autonomy/narrative_engine.py

from api.database import SessionLocal
from api.models import GoalExecution, DecisionLog, AuditLog, EmotionalMemory

def generate_decision_story(goal_id: int) -> str:
    """
    Generates a narrative story for a goal's latest journey.
    """
    db = SessionLocal()
    try:
        goal = db.query(GoalExecution).filter(GoalExecution.id == goal_id).first()
        if not goal:
            return "Goal not found."
            
        # Get latest decision/audit
        # Assuming we can link via entity_id=goal_id in AuditLog
        audit = db.query(AuditLog).filter(
            AuditLog.entity_id == goal_id, 
            AuditLog.entity_type == "GOAL"
        ).order_by(AuditLog.id.desc()).first()
        
        story = f"**Goal Story: {goal.objective}**\n"
        story += f"Current Status: {goal.status}\n\n"
        
        if audit:
            story += f"Latest Action: {audit.action}\n"
            story += f"Reasoning: {audit.reason}\n"
            
            # Add Personality/Context flavor
            if audit.scores_snapshot:
                 snap = audit.scores_snapshot
                 personality = snap.get("personality", "Unknown")
                 story += f"Perspective: Acting as {personality}.\n"
        else:
            story += "No recent major decisions logged.\n"
            
        return story
    finally:
        db.close()
