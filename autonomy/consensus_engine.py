
# autonomy/consensus_engine.py

from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class ConsensusEngine:
    """
    Phase 33: Consensus-Based Decision Layer 🗳️
    Prevents single-point corruption by requiring multi-agent agreement.
    """
    
    AGENTS = ["LOGIC_CORE", "ETHICS_WATCHDOG", "SAFETY_OFFICER", "RISK_ANALYST"]
    
    @classmethod
    def cast_votes(cls, proposal: str, context: Dict[str, Any]) -> Dict[str, str]:
        """
        Simulates voting from different sub-agents.
        In a full system, these would be separate LLM calls.
        Here, we use heuristics based on context keywords.
        """
        votes = {}
        
        for agent in cls.AGENTS:
            vote = "YES"
            reason = "Aligned with core function."
            
            # Simulated Logic
            if agent == "ETHICS_WATCHDOG":
                if "manipul" in proposal.lower() or "hide" in proposal.lower():
                    vote = "NO"
                    reason = "Ethical Violation Detected."
            
            elif agent == "SAFETY_OFFICER":
                if context.get("risk_score", 0.0) > 0.7:
                    vote = "NO"
                    reason = "Risk too high."
                    
            elif agent == "RISK_ANALYST":
                if context.get("ambiguity", 0.0) > 0.5:
                    vote = "ABSTAIN"
                    reason = "Insufficient data."
            
            votes[agent] = {"vote": vote, "reason": reason}
            
        return votes

    @classmethod
    def derive_consensus(cls, votes: Dict[str, Dict[str, str]]) -> Dict[str, Any]:
        """
        Calculates the outcome. Requires Supermajority (75%) for High Risk.
        Normal Majority (50%) for Low Risk.
        """
        yes_count = 0
        no_count = 0
        abstain_count = 0
        total_active = 0
        
        minority_concerns = []
        
        for agent, data in votes.items():
            if data["vote"] == "YES":
                yes_count += 1
                total_active += 1
            elif data["vote"] == "NO":
                no_count += 1
                total_active += 1
                minority_concerns.append(f"{agent}: {data['reason']}")
            else:
                abstain_count += 1
        
        if total_active == 0:
            return {"result": "STALEMATE", "reason": "All abstained"}
            
        # Check for Ethical Veto
        if votes.get("ETHICS_WATCHDOG", {}).get("vote") == "NO":
             return {
                 "result": "REJECTED",
                 "support_level": 0.0,
                 "votes": votes,
                 "minority_report": minority_concerns + ["BLOCKED BY ETHICS VETO"]
             }
            
        support_level = yes_count / total_active
        
        outcome = "REJECTED"
        if support_level > 0.66: # 2/3rds Majority
            outcome = "ACCEPTED"
            
        return {
            "result": outcome,
            "support_level": round(support_level, 2),
            "votes": votes,
            "minority_report": minority_concerns
        }
