
# autonomy/meta_cognition_engine.py

import logging
from typing import Dict, Any, List
from api.database import SessionLocal
from api.models import EvolutionDirective

logger = logging.getLogger(__name__)

def evaluate_decision_quality(decision: Dict[str, Any], context: str) -> Dict[str, Any]:
    """
    Reflects on a decision *after* it is made (or simulating it).
    Ask: Was this strategic or reactive?
    """
    score = decision.get("confidence", 0.0)
    decision_type = decision.get("decision", "NONE")
    
    evaluation = {
        "judgment": "NEUTRAL",
        "reason": "Standard operation.",
        "future_rule": "ALLOW"
    }
    
    # 1. Check for Reactive Panic
    # If decision was "KILL" with low confidence -> Panic
    if decision_type == "KILL" and score < 0.3:
        evaluation["judgment"] = "POOR"
        evaluation["reason"] = "Reactive kill without sufficient confidence."
        evaluation["future_rule"] = "RESTRICT"
        
    # 2. Check for Strategic Silence
    # If decision was "NONE" but score was high? (Not possible in current logic but conceptually)
    # If "PAUSE" led to resource conservation -> GOOD
    
    return evaluation

def should_remain_silent(current_instability: float, noise_level: float) -> bool:
    """
    Phase 30.5: Silence Mode.
    If Noise > Signal, or Instability High -> SILENCE.
    """
    # Simple heuristic
    if current_instability > 0.8:
        return True # Too unstable to act
        
    if noise_level > 0.7:
        return True # Too much noise
        
    return False

def record_evolution_directive(source: str, change_type: str, reason: str, risk: float):
    """
    Writes a self-evolution directive to DB.
    """
    db = SessionLocal()
    try:
        directive = EvolutionDirective(
            source=source,
            change_type=change_type,
            reason=reason,
            risk_level=risk
        )
        db.add(directive)
        db.commit()
        logger.info(f"🧬 EVOLUTION DIRECTIVE: {change_type} - {reason}")
    except Exception as e:
        logger.error(f"Failed to record evolution: {e}")
    finally:
        db.close()
