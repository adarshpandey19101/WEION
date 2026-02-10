
# autonomy/arbitrator.py

import logging
from api.database import SessionLocal
from api.models import UserRole

logger = logging.getLogger(__name__)

# Role Weights
ROLE_WEIGHTS = {
    "OWNER": 1.0,
    "ADMIN": 0.8,
    "MANAGER": 0.6,
    "CONTRIBUTOR": 0.3
}

DEFAULT_ROLE = "CONTRIBUTOR"

def get_user_role(user_id: str) -> str:
    """Fetches user role from DB or returns default."""
    db = SessionLocal()
    try:
        user_role = db.query(UserRole).filter(UserRole.user_id == user_id).first()
        if user_role:
            return user_role.role
        return DEFAULT_ROLE
    finally:
        db.close()

def calculate_role_score(user_id: str) -> float:
    """
    Returns the arbitration weight for a specific user.
    """
    role = get_user_role(user_id)
    return ROLE_WEIGHTS.get(role, 0.3)
