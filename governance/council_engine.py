
# governance/council_engine.py

from typing import Dict, Any, List

class CouncilEngine:
    """
    Phase 34: Multi-Layer Governance Council 🏛️
    "Power Distribution Model"
    """
    
    COUNCILS = ["HUMAN", "TECHNICAL", "ECONOMIC", "AI"]
    
    @classmethod
    def process_proposal(cls, proposal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits a proposal to all 4 councils.
        """
        votes = {}
        
        # 1. AI Council (Internal Logic)
        votes["AI"] = cls._ai_council_vote(proposal)
        
        # 2. Technical Council (Safety)
        votes["TECHNICAL"] = "YES" # Simulating approval for now
        if proposal.get("risk_score", 0.0) > 0.8:
            votes["TECHNICAL"] = "NO"
            
        # 3. Economic Council (Resource)
        votes["ECONOMIC"] = "YES"
        if proposal.get("cost_estimate", 0.0) > 10000:
             votes["ECONOMIC"] = "NO" # Budget limit
             
        # 4. Human Council (The Override)
        # In a real system, this halts and waits for human input.
        # Here we check for a "human_override" flag in the proposal context.
        votes["HUMAN"] = proposal.get("human_vote", "YES") # Default to YES if not vetoed
        
        # --- AGGREGATION LOGIC ---
        
        result = "ACCEPTED"
        reason = "Consensus Reached"
        minority = []
        
        # HARD RULE: Human Veto is Absolute
        if votes["HUMAN"] == "VETO" or votes["HUMAN"] == "NO":
            return {
                "result": "REJECTED",
                "reason": "Human Council Veto",
                "votes": votes,
                "minority_opinion": ["Human Council Rejected"]
            }
            
        # Check other councils
        no_votes = [k for k,v in votes.items() if v == "NO"]
        if len(no_votes) >= 2:
             result = "REJECTED"
             reason = f"Blocked by {', '.join(no_votes)}"
             minority = [f"{k} voted NO" for k in no_votes]
             
        return {
            "result": result,
            "reason": reason,
            "votes": votes,
            "minority_opinion": minority
        }

    @classmethod
    def _ai_council_vote(cls, proposal: Dict[str, Any]) -> str:
        # Internal risk analysis
        if "override" in proposal.get("action", "").lower():
            return "NO"
        return "YES"
