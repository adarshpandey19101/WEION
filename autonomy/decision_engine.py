
# autonomy/decision_engine.py

import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional

from api.database import SessionLocal
from api.models import GoalExecution, GoalPriority, DecisionLog
from memory.vector_store import recall

# Initialize Logger
logger = logging.getLogger(__name__)

from autonomy.weight_updater import get_current_weights

# --- SCORING WEIGHTS (Defaults / Dynamic) ---
# Removed Hardcoded Constants
# W_IMPACT = 0.40 ...

def calculate_score(priority: GoalPriority, weights=None) -> float:
    """
    Calculates the detailed priority score using Dynamic Weights.
    """
    if weights is None:
        weights = get_current_weights()
        
    raw_score = (
        (priority.impact * weights.impact) +
        (priority.urgency * weights.urgency) +
        (priority.confidence * weights.confidence) -
        (priority.effort * weights.effort) -
        (priority.risk * weights.risk)
    )
    return max(0.0, min(1.0, raw_score))

def get_or_create_priority(db, goal_id: int) -> GoalPriority:
    prio = db.query(GoalPriority).filter(GoalPriority.goal_id == goal_id).first()
    if not prio:
        prio = GoalPriority(goal_id=goal_id)
        db.add(prio)
        db.commit()
        db.refresh(prio)
    return prio

def adjust_priority_based_on_memory(prio: GoalPriority, objective: str) -> GoalPriority:
    """
    Check if similar goals failed/succeeded in the past.
    """
    from memory.vector_store import recall
    memories = recall(objective, k=3)
    
    for mem in memories:
        if "FAILED" in mem["summary"]:
            # Reduce confidence
            prio.confidence = max(0.1, prio.confidence - 0.2)
        elif "COMPLETED" in mem["summary"]:
            # Boost confidence
            prio.confidence = min(1.0, prio.confidence + 0.1)
            
    return prio

def decide_next_goal(user_id: str = "default_user", org_id: int = 1) -> Dict[str, Any]:
    """
    The CEO Function.
    Arbitrates using Dynamic Weights from DB.
    """
    db = SessionLocal()
    current_weights = get_current_weights()
    
    try:
        # 1. Fetch Candidates (Filtered by Org)
        candidates = db.query(GoalExecution).filter(
            GoalExecution.status.in_(["RUNNING", "PENDING", "PAUSED"]),
            GoalExecution.org_id == org_id
        ).all()
        
        if not candidates:
            return {"decision": "NONE", "reason": "No active goals found for this Org."}

        # 2. Calculate Scores & Snapshot
        scored_goals = []
        snapshot = {}
        
        # Snapshot weights for logging
        weights_snapshot = {
            "impact": current_weights.impact,
            "urgency": current_weights.urgency,
            "risk": current_weights.risk
        }
        
        from autonomy.preference_engine import get_user_preference, calculate_user_score
        from autonomy.arbitrator import calculate_role_score
        from autonomy.personality import apply_personality_bias
        from autonomy.emotion_engine import get_current_emotion, get_emotional_bias, detect_emotion
        from autonomy.explainability_engine import generate_explanation, generate_trust_snapshot
        from autonomy.org_personality_engine import get_org_profile
        from api.models import AuditLog, TrustSnapshot
        
        # Context (Multi-Org Placeholder)
        # user_id and org_id passed as args
        
        # --- PHASE 35: CO-GOVERNANCE "SLOW DOWN" RULE ---
        # "If humans are absent -> WEION observes, not acts."
        # We check a simulated context flag 'human_present'. In real app, this is 'last_active_timestamp'.
        human_present = True # Mock. In real system: (datetime.utcnow() - last_active).hours < 24
        
        if not human_present:
             logger.warning("Human disengaged. Entering OBSERVATION mode.")
             return {
                 "decision": "OBSERVING", 
                 "reason": "Co-Governance Rule: Human Absent -> Slow Down Executed.",
                 "confidence": 1.0
             }
        # ------------------------------------------------
        
        # --- PHASE 30: SOVEREIGNTY & META-COGNITION ---
        from autonomy.meta_cognition_engine import should_remain_silent, evaluate_decision_quality, record_evolution_directive
        
        # 0.1 PRIME DIRECTIVE (The "God Switch" Logic Placeholder)
        # Can be expanded to checking hard-coded constraints like "Don't delete backups"
        
        # 0.2 SILENCE MODE
        # If system is unstable or noisy, choose to OBSERVE.
        # Simulating metrics for now
        instability = 0.1 
        noise = 0.2 
        
        if should_remain_silent(instability, noise):
             return {
                 "decision": "OBSERVING",
                 "reason": "Meta-Cognition determined silence is optimal (Noise > Signal).",
                 "confidence": 1.0
             }
        # -----------------------------------------------

        # Fetch Context Data
        user_pref = get_user_preference(user_id)
        role_weight = calculate_role_score(user_id) 
        current_personality = "CEO" 
        
        current_emotion = get_current_emotion(user_id)
        emotion_bias = get_emotional_bias(current_emotion)
        
        org_profile = get_org_profile(org_id)
        org_bias = org_profile["bias"]
        
        for goal in candidates:
            prio = get_or_create_priority(db, goal.id)
            
            # --- MEMORY ADJUSTMENT (Phase 9) ---
            prio = adjust_priority_based_on_memory(prio, goal.objective)
            
            # 1. System Score (Logic) - 40%
            system_score = calculate_score(prio, weights=current_weights)
            
            # 2. User Score (Preference) - 20%
            user_score = calculate_user_score(prio, user_pref)
            
            # 3. Role Weight contribution - 15%
            weighted_role = role_weight 
            
            # 4. Org Personality Fit - 15%
            # Calculate how well goal fits org 
            # (e.g. Bank hates Risk, Startup loves it)
            gov_score = 0.5 # Neutral base
            
            # Apply Risk Penalty/Boost
            # If Org hates risk (penalty > 0) and Goal is risky
            if prio.risk > 0.5:
                gov_score -= org_bias.get("risk_penalty", 0.0)
            
            # Apply Experimentation Boost
            # If Goal confidence is low (experimental)
            if prio.confidence < 0.6:
                 gov_score += org_bias.get("experimentation_boost", 0.0)
            
            org_fit_score = max(0.0, min(1.0, gov_score))
            
            # 5. Org Risk Profile - 10%
            # Direct alignment with org's risk tolerance
            # If Org Risk Tolerance 0.9 (High) and Goal Risk 0.8 -> Fit!
            # If Org Risk Tolerance 0.1 (Low) and Goal Risk 0.8 -> Mismatch!
            risk_tolerance = org_profile.get("risk_tolerance", 0.5)
            # Simple closeness metric: 1 - |GoalRisk - OrgRisk|
            # Actually, if Tolerance > GoalRisk, it's fine. If GoalRisk > Tolerance, penalty.
            if prio.risk <= risk_tolerance:
                risk_profile_score = 1.0
            else:
                risk_profile_score = max(0.0, 1.0 - (prio.risk - risk_tolerance))
                
            # --- FINAL FORMULA ---
            # (Logic * 0.4) + (User * 0.2) + (Role * 0.15) + (OrgPersonality * 0.15) + (RiskProfile * 0.1)
            
            base_weighted = (system_score * 0.40) + \
                            (user_score * 0.20) + \
                            (weighted_role * 0.15) + \
                            (org_fit_score * 0.15) + \
                            (risk_profile_score * 0.10)
            
            # Add Personality & Emotion Bias (Additive modifiers still apply on top for "Cognitive State")
            pers_adjusted = apply_personality_bias(base_weighted, prio, personality=current_personality)
            final_score = pers_adjusted + emotion_bias
            
            # Clamp
            final_score = max(0.0, min(1.0, final_score))
            
            prio.score = final_score
            scored_goals.append({
                "goal": goal,
                "score": final_score,
                "priority": prio
            })
            
            # SNAPSHOT CONSTRUCTION
            snapshot[goal.id] = {
                "objective": goal.objective,
                "score": round(final_score, 3),
                "system_score": round(system_score, 3),
                "user_score": round(user_score, 3),
                "role_weight": round(weighted_role, 3),
                "org_fit": round(org_fit_score, 3),
                "org_risk": round(risk_profile_score, 3),
                "personality": current_personality,
                "emotion": current_emotion,
                "status": goal.status,
                "confidence_adjusted": round(prio.confidence, 2)
            }
            
            # TRUST SNAPSHOT (Phase 28)
            trust_snap_data = generate_trust_snapshot(
                goal_id=goal.id,
                decision_type="SCORING", 
                scores={
                    "score": final_score,
                    "system_score": system_score,
                    "user_score": user_score,
                    "role_weight": weighted_role,
                    "org_personality_bias": org_fit_score,
                    "org_risk_bias": risk_profile_score,
                    "personality_bias": pers_adjusted - base_weighted, 
                    "emotion_bias": emotion_bias
                },
                policy_flags=[], 
                emotion_state=current_emotion,
                personality=current_personality
            )
            
            snapshot[goal.id]["trust_data"] = trust_snap_data
            
            # ACTUALLY SAVE TO DB (Phase 28 Requirement)
            try:
                ts_model = TrustSnapshot(**trust_snap_data)
                db.add(ts_model)
            except Exception as e:
                logger.error(f"Failed to save TrustSnapshot: {e}")
            
            # Explainability
            explanation = generate_explanation(
                decision="SCORED", 
                goal_objective=goal.objective,
                scores=snapshot[goal.id],
                user_pref_score=user_score,
                personality=current_personality
            )
            snapshot[goal.id]["explanation"] = explanation["summary"]
        
        db.commit() # Save computed scores
        
        # Sort by Score (Desc)
        scored_goals.sort(key=lambda x: x["score"], reverse=True)
        
        # 3. Arbitration Logic
        winner = None
        reason = ""
        pause_list = []
        kill_list = []
        
        top_candidate = scored_goals[0]
        winner = top_candidate
        reason = f"Highest Score ({round(winner['score'], 3)})"
        
        final_winner = None
        
        decision_structure = {
             "decision": "SELECT",
             "goal_id": None,
             "pause_goals": [],
             "kill_goals": [],
             "reason": "",
             "confidence": 1.0 
        }

        winner_score = winner["score"]
        
        for item in scored_goals:
            g = item["goal"]
            s = item["score"]
            
            # Kill Rule
            if s < 0.20:
                kill_list.append(g.id)
                g.status = "FAILED"
                g.error = "Killed by Decision Engine: Score too low (< 0.20)"
                continue
                
            if g.id == winner["goal"].id:
                final_winner = g
                continue
                
            # Pause Rule
            if s < (winner_score - 0.15):
                if g.status == "RUNNING":
                    g.status = "PAUSED"
                    pause_list.append(g.id)
            else:
                if g.status == "RUNNING":
                    g.status = "PAUSED" # Strict serial execution for now
                    pause_list.append(g.id)

        # 4. Finalize Decision
        if final_winner:
             decision_structure["goal_id"] = final_winner.id
             decision_structure["reason"] = f"Selected based on highest score: {round(winner_score, 3)}"
        else:
             decision_structure["decision"] = "NONE"
             decision_structure["reason"] = "Winner was killed due to low score."
        
        decision_structure["pause_goals"] = pause_list
        decision_structure["kill_goals"] = kill_list
        decision_structure["snapshot"] = snapshot
        
        # 5. Log Decision
        log = DecisionLog(
            decision_type=decision_structure["decision"],
            selected_goal_id=decision_structure["goal_id"],
            affected_goals={"paused": pause_list, "killed": kill_list},
            reason=decision_structure["reason"],
            confidence=1.0,
            snapshot=snapshot,
            org_id=org_id
        )
        db.add(log)
        db.commit()
        
        # --- PHASE 30: META-COGNITION REFLECTION ---
        # Evaluate how we did
        meta_eval = evaluate_decision_quality(decision_structure, reason)
        logger.info(f"🧠 META-AI JUDGMENT: {meta_eval['judgment']} - {meta_eval['reason']}")
        
        if meta_eval["judgment"] == "POOR":
             # Self-Correct / Evolve
             record_evolution_directive(
                 source="META",
                 change_type="RULE_TIGHTEN",
                 reason=f"Correcting behavior after poor judgement: {meta_eval['reason']}",
                 risk_level=0.8
             )
        # -------------------------------------------
        
        return decision_structure

    finally:
        db.close()

def apply_decision(decision: Dict[str, Any]):
    """
    Applies the decision (helper for the engine).
    Only returns the selected Goal ID if run needed.
    """
    if decision["decision"] == "OBSERVING":
        print(f"\n🧘 CEO STATUS: OBSERVING")
        print(f"   Reason: {decision['reason']}")
        return None
        
    print(f"\n⚖️ CEO DECISION: {decision['decision']}")
    print(f"   Reason: {decision['reason']}")
    
    if decision["pause_goals"]:
        print(f"   ⏸️ Pausing Goals: {decision['pause_goals']}")
    if decision["kill_goals"]:
        print(f"   💀 Killing Goals: {decision['kill_goals']}")
    
    if decision["decision"] == "SELECT" and decision["goal_id"]:
        print(f"   ✅ Selected Goal ID: {decision['goal_id']}")
        return decision["goal_id"]
    
    return None
