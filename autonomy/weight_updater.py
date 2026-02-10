
# autonomy/weight_updater.py

import logging
from typing import Dict, Any
from api.database import SessionLocal
from api.models import PriorityWeights

logger = logging.getLogger(__name__)

# --- SAFETY CONSTANTS ---
MIN_WEIGHT = 0.05
MAX_WEIGHT = 0.6
MAX_STEP_CHANGE = 0.05

def get_current_weights() -> PriorityWeights:
    """Fetches the latest weights or creates default."""
    db = SessionLocal()
    try:
        weights = db.query(PriorityWeights).order_by(PriorityWeights.id.desc()).first()
        if not weights:
            weights = PriorityWeights()
            db.add(weights)
            db.commit()
            db.refresh(weights)
        return weights
    finally:
        db.close()

def update_priority_weights(adjustments: Dict[str, float]):
    """
    Safely updates priority weights based on suggested adjustments.
    adjustments: dict like {"impact": 0.02, "risk": -0.01}
    """
    db = SessionLocal()
    try:
        # Get latest (we create a NEW record for every update to keep history? 
        # Or update existing? "Weight Updater" usually implies evolution. 
        # Adding a new row is safer for history/auditing.
        
        last = db.query(PriorityWeights).order_by(PriorityWeights.id.desc()).first()
        if not last:
            last = PriorityWeights() # Defaults
            
        new_weights = PriorityWeights(
            impact=last.impact,
            urgency=last.urgency,
            confidence=last.confidence,
            effort=last.effort,
            risk=last.risk
        )
        
        updates_made = False
        
        for key, delta in adjustments.items():
            if not hasattr(new_weights, key):
                continue
                
            current_val = getattr(new_weights, key)
            
            # 1. Cap Step Change
            safe_delta = max(-MAX_STEP_CHANGE, min(MAX_STEP_CHANGE, delta))
            
            # 2. Apply
            new_val = current_val + safe_delta
            
            # 3. Clamp Range
            new_val = max(MIN_WEIGHT, min(MAX_WEIGHT, new_val))
            
            if abs(new_val - current_val) > 1e-5:
                setattr(new_weights, key, new_val)
                logger.info(f"⚖️ Weight Update: {key} {current_val:.3f} -> {new_val:.3f} (Delta: {safe_delta})")
                updates_made = True
                
        if updates_made:
            db.add(new_weights)
            db.commit()
            print("\n⚖️ Global Priority Weights Updated.")
        else:
            print("\n⚖️ No significant weight changes required.")
            
    except Exception as e:
        logger.error(f"Weight Update Failed: {e}")
    finally:
        db.close()
