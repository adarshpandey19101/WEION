
# autonomy/personality.py

from typing import Dict, Any

# Personality Profiles
# Bias values added to scores if conditions match
PERSONALITY_PROFILES = {
    "CEO": {
        "impact_bonus": 0.2,    # Loves High Impact
        "urgency_bonus": 0.1,   # Likes Speed
        "risk_penalty": 0.1,    # Dislikes Failure
        "effort_penalty": 0.1   # Wants Low Effort / High ROI
    },
    "CTO": {
        "impact_bonus": 0.1,
        "confidence_bonus": 0.2, # Loves Certainty
        "risk_penalty": 0.3,     # Hates technical debt/risk
        "urgency_bonus": -0.1    # Dislikes rushing
    },
    "RESEARCHER": {
        "experimentation_bonus": 0.3, # Loves novelty (Low Confidence is ok)
        "urgency_bonus": -0.2,        # Wants time to think
        "risk_penalty": -0.1          # Ok with failure
    }
}

DEFAULT_PERSONALITY = "CEO" # Default mode

def apply_personality_bias(
    base_score: float, 
    priority: Any, 
    personality: str = DEFAULT_PERSONALITY
) -> float:
    """
    Adjusts the score based on the system's "Persona".
    """
    
    profile = PERSONALITY_PROFILES.get(personality, PERSONALITY_PROFILES[DEFAULT_PERSONALITY])
    score = base_score
    
    # 1. Impact Bias
    if priority.impact > 0.7:
        score += profile.get("impact_bonus", 0)
        
    # 2. Urgency Bias
    if priority.urgency > 0.7:
        score += profile.get("urgency_bonus", 0)
        
    # 3. Risk Bias (Penalty or Bonus)
    if priority.risk > 0.6:
        # If profile has risk_penalty > 0, we subtract it.
        # If profile has risk_penalty < 0 (negative penalty = bonus), we subtract negative = add.
        score -= profile.get("risk_penalty", 0)
        
    # 4. Confidence Bias
    if priority.confidence > 0.8:
        score += profile.get("confidence_bonus", 0)
        
    # 5. Experimentation Logic (Researcher Special)
    if "experimentation_bonus" in profile:
        # If Confidence is Low but Impact is decent -> Researcher loves it
        if priority.confidence < 0.6 and priority.impact > 0.4:
            score += profile["experimentation_bonus"]
            
    return max(0.0, min(1.0, score))
