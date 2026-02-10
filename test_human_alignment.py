
# test_human_alignment.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.models import GoalPriority, UserPreference
from autonomy.preference_engine import calculate_user_score

def test_risk_alignment():
    print("\n--- Test: Human Alignment (Risk Tolerance) ---")
    
    # Goal: High Risk (0.8)
    # System Score would be penalized (-0.2 * 0.8 = -0.16)
    prio_risky = GoalPriority(
        impact=0.8, 
        urgency=0.5, 
        confidence=0.5, 
        risk=0.8, # Very Risky
        effort=0.5
    )
    
    # ---------------------------------------------------------
    # Scenario A: Risk Taker (Elon Mode)
    # ---------------------------------------------------------
    user_risky = UserPreference(
        user_id="elon",
        pref_speed_vs_quality=0.8,
        pref_risk_tolerance=0.9, # Loves Risk
        pref_experimentation=0.9
    )
    
    score_risky = calculate_user_score(prio_risky, user_risky)
    print(f"\nUser: Risk Taker (0.9)")
    print(f"Goal Risk: 0.8")
    print(f"User Score: {score_risky}")
    
    # Logic: Neutral 0.5 + Bonus 0.1 (Risk>0.5 & Pref>0.6) = 0.6 minimum
    # Plus maybe speed bonus? Urgency is 0.5 so neutral.
    assert score_risky > 0.5, "Risk Taker should boost Risky Goal"

    # ---------------------------------------------------------
    # Scenario B: Conservative User (Banker Mode)
    # ---------------------------------------------------------
    user_safe = UserPreference(
        user_id="banker",
        pref_speed_vs_quality=0.2,
        pref_risk_tolerance=0.1, # Hates Risk
        pref_experimentation=0.1
    )
    
    score_safe = calculate_user_score(prio_risky, user_safe)
    print(f"\nUser: Conservative (0.1)")
    print(f"Goal Risk: 0.8")
    print(f"User Score: {score_safe}")
    
    # Logic: Neutral 0.5 - Penalty
    # Penalty: (0.8 - 0.4) * (0.5 - 0.1) * 4.0 = 0.4 * 0.4 * 4.0 = 0.64
    # Score = 0.5 - 0.64 = -0.14 -> Clamped to 0.0
    assert score_safe < 0.5, "Conservative User should penalize Risky Goal"
    assert score_safe < score_risky, "Risk Taker score should be higher than Conservative score"

    print(f"\n✅ Alignment Verified: Score Diff {score_risky - score_safe:.2f}")

if __name__ == "__main__":
    test_risk_alignment()
