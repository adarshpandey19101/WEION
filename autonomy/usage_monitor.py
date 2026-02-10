
# autonomy/usage_monitor.py

import logging
from api.database import SessionLocal
from api.models import UsageLog

logger = logging.getLogger(__name__)

COST_PER_ACTION = 0.01
COST_PER_DECISION = 0.05

def log_usage(user_id: str, action: str, tokens: int = 0):
    """
    Logs usage metrics for billing/analytics.
    """
    db = SessionLocal()
    try:
        # Simple Cost Model
        cost = 0.0
        if action == "goal_run":
            cost = COST_PER_ACTION
        elif action == "decision":
            cost = COST_PER_DECISION
            
        entry = UsageLog(
            user_id=user_id,
            action=action,
            tokens=tokens,
            cost=cost
        )
        db.add(entry)
        db.commit()
        # logger.info(f"💰 Usage Logged: {action} by {user_id} (${cost})")
    except Exception as e:
        logger.error(f"Usage Logging Failed: {e}")
    finally:
        db.close()
