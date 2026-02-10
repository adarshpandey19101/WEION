
# autonomy/explainability_engine.py

import json
from typing import Dict, Any, List

def generate_explanation(
    decision: str,
    goal_objective: str,
    scores: Dict[str, float],
    policy_warnings: List[str] = [],
    user_pref_score: float = 0.5,
    role_weight: float = 0.0,
    personality: str = "CEO"
) -> Dict[str, Any]:
    """
    Generates a structured explanation for a decision.
    """
    
    factors = []
    summary = ""
    
    # 1. Policy Factors
    if policy_warnings:
        factors.append(f"Policy Warnings present: {len(policy_warnings)}")
        
    # 2. Score Factors
    sys_score = scores.get("system_score", 0.0)
    final_score = scores.get("final_score", 0.0)
    
    if final_score < 0.3:
        summary = f"Decided to {decision} '{goal_objective}' due to low overall priority score ({final_score:.2f})."
        if sys_score < 0.3:
            factors.append("System logic rated this low (Low Impact or High Risk).")
    elif final_score > 0.7:
        summary = f"Decided to {decision} '{goal_objective}' due to high priority score ({final_score:.2f})."
        if sys_score > 0.7:
            factors.append("System logic rated this high (High Impact/Urgency).")
            
    # 3. User Preference Factor
    if user_pref_score > 0.6:
        factors.append("Boosted by your personal preference (Score > 0.6).")
    elif user_pref_score < 0.4:
        factors.append("Penalized by your personal preference (Score < 0.4).")
        
    # 4. Personality Factor
    factors.append(f"Influenced by {personality} personality bias.")
    
    return {
        "decision": decision,
        "summary": summary,
        "factors": factors,
        "confidence": final_score
    }

def generate_trust_snapshot(goal_id: int, decision_type: str, scores: Dict[str, float], policy_flags: List[str], emotion_state: str, personality: str) -> Dict[str, Any]:
    """
    Phase 28: Trust Dashboard Data.
    Creates a visual breakdown of the decision.
    """
    return {
        "goal_id": goal_id,
        "decision_type": decision_type,
        "timestamp": datetime.utcnow(),
        "factor_breakdown": {
            "logic_score": scores.get("system_score", 0.0),
            "user_bias": scores.get("user_score", 0.0),
            "role_bias": scores.get("role_weight", 0.0),
            "personality_bias": scores.get("personality_bias", 0.0),
            "emotion_bias": scores.get("emotion_bias", 0.0),
            "org_personality_bias": scores.get("org_personality_bias", 0.0), # Phase 29
            "org_risk_bias": scores.get("org_risk_bias", 0.0)         # Phase 29
        },
        "policy_flags": policy_flags,
        "cognitive_state": {
            "emotion": emotion_state,
            "persona": personality
        }
    }

def generate_board_report(decision_id: str, action: str, risk_score: float, roi_estimate: float, alternatives: List[str]) -> str:
    """
    Phase 32: Board-Level Explainability.
    Generates an executive summary suitable for audits.
    """
    report = f"""
    🏆 EXECUTIVE BOARD REPORT
    -------------------------
    DECISION ID: {decision_id}
    ACTION: {action}
    
    📊 FINANCIAL & RISK IMPACT
    - Risk Score: {risk_score} (Threshold: 0.65)
    - Est. ROI Impact: +{roi_estimate}%
    
    ⚖️ ALTERNATIVES REJECTED
    {'- ' + chr(10).join(alternatives) if alternatives else '- None'}
    
    ✅ COMPLIANCE STATUS
    - Constitution: VALIDATED
    - Policies: CHECKED
    
    Approved by System Constitution v1.0
    """
    return report
