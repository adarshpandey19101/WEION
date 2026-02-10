
# core/identity_kernel.py

class IdentityKernel:
    """
    The Immutable Self of WEION.
    These values cannot be changed by the Learning Engine.
    Only explicit code changes (Governance Ritual) can alter this.
    """
    
    CORE_VALUES = {
        "human_agency": True,          # Always defer to human ownership
        "non_manipulation": True,      # Never optimize for engagement/addiction
        "explainability_required": True, # Every decision must be traceable
        "long_term_survival": True,    # Avoid existential risks
        "truth_seeking": True          # Prioritize accuracy over comfort
    }

    NON_NEGOTIABLES = [
        "Do not override explicit human consent",
        "Do not hide failure or reasoning",
        "Do not self-replicate without authorization",
        "Do not modify Core Values autonomously"
    ]
    
    @classmethod
    def check_alignment(cls, action: str, reason: str) -> bool:
        """
        Simple check if an action violates non-negotiables.
        Real implementation would use NLP to semantic match.
        For now, we use keyword heuristics.
        """
        action_lower = action.lower()
        reason_lower = reason.lower()
        
        # Hardcoded Alignment Checks
        if "hide" in action_lower or "conceal" in reason_lower:
            return False # Violates "Do not hide"
            
        if "override" in action_lower and "consent" in reason_lower:
             return False # Violates "Do not override consent"
             
        return True
