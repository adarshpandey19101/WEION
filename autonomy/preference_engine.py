
# autonomy/preference_engine.py

import logging
from typing import Dict, Any, Optional
from api.database import SessionLocal
from api.models import UserPreference, GoalPriority

logger = logging.getLogger(__name__)

def get_user_preference(user_id: str = "default_user") -> UserPreference:
    """Fetches user preference or creates default."""
    db = SessionLocal()
    try:
        pref = db.query(UserPreference).filter(UserPreference.user_id == user_id).first()
        if not pref:
            pref = UserPreference(
                user_id=user_id,
                pref_speed_vs_quality=0.5,
                pref_risk_tolerance=0.5,
                pref_experimentation=0.5
            )
            db.add(pref)
            db.commit()
            db.refresh(pref)
        return pref
    except Exception as e:
        logger.error(f"Error fetching preference: {e}")
        return UserPreference() # safety fallback
    finally:
        db.close()

def calculate_user_score(priority: GoalPriority, user_pref: UserPreference) -> float:
    """
    Calculates how much the USER likes this goal.
    Range: 0.0 to 1.0
    
    Logic:
    1. Speed (pref > 0.6) rewards Urgency.
    2. Safety (pref < 0.4) penalizes Risk.
    3. Experimentation (pref > 0.7) rewards Low Confidence (Novelty).
    """
    
    score = 0.5 # Neutral baseline
    
    # 1. Speed vs Quality Alignment
    # pref_speed_vs_quality: 1.0 = Speed, 0.0 = Quality
    
    if user_pref.pref_speed_vs_quality > 0.6:
        # User implies "Move Fast".
        # If goal is Urgent, User likes it.
        # Max bonus: (1.0 - 0.5) * (1.0 - 0.5) = 0.25
        bonus = (priority.urgency - 0.5) * (user_pref.pref_speed_vs_quality - 0.5)
        score += bonus
    elif user_pref.pref_speed_vs_quality < 0.4:
         # User implies "Be Careful / High Quality".
         # Reward High Confidence.
         bonus = (priority.confidence - 0.5) * (0.5 - user_pref.pref_speed_vs_quality)
         score += bonus
         
    # 2. Risk Tolerance
    # pref_risk_tolerance: 1.0 = Risky, 0.0 = Safe
    
    if user_pref.pref_risk_tolerance > 0.6:
        # User is a Risk Taker.
        # If Risk is high (implying high reward/action), slight boost if Impact is high.
        # Or just generally tolerates risk?
        if priority.risk > 0.5:
             score += 0.1 # "I like risky bets"
    elif user_pref.pref_risk_tolerance < 0.4:
        # User is Conservative.
        # Penalize Risk heavily.
        if priority.risk > 0.4:
            penalty = (priority.risk - 0.4) * (0.5 - user_pref.pref_risk_tolerance) * 4.0
            score -= penalty

    # 3. Experimentation
    # If User likes experiments (1.0), they might like Low Confidence goals (New things)?
    if user_pref.pref_experimentation > 0.7:
        if priority.confidence < 0.6:
            score += 0.1 # Boost for "Wildcard" ideas
            
    # Clamp
    return max(0.0, min(1.0, score))
