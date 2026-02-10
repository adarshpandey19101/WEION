
# autonomy/policy_engine.py

import logging
from typing import List, Dict, Any, Tuple
from api.database import SessionLocal
from api.models import OrgPolicy

logger = logging.getLogger(__name__)

def get_active_policies() -> List[OrgPolicy]:
    db = SessionLocal()
    try:
        return db.query(OrgPolicy).filter(OrgPolicy.active == True).all()
    finally:
        db.close()

def check_policy_compliance(action_description: str) -> Tuple[bool, str, List[str]]:
    """
    Checks if an action violates any active policies.
    Returns: (is_compliant, blocking_reason, warnings)
    """
    policies = get_active_policies()
    warnings = []
    
    # Simple Keyword Matching Logic (V1)
    # In V2, use LLM or Semantic Search
    
    for policy in policies:
        # Check rule match
        # Assuming policy.rule is like "No upload to public repo"
        # We need simpler logic for code-based check without LLM parsing every time
        # Let's assume policy.rule contains keywords to ban.
        
        # Example Policy Rule: "BAN: public_upload"
        # Example Action: "Upload file to public S3"
        
        # Heuristic: Check if policy keywords appear in action
        # For this prototype: Assume policy.rule IS the forbidden keyword/phrase
        forbidden_phrase = policy.rule.lower()
        if forbidden_phrase in action_description.lower():
            reason = f"Policy Violation ({policy.category}): Found '{forbidden_phrase}'"
            
            if policy.severity == "HARD":
                logger.error(f"⛔ POLICY BLOCK: {reason}")
                return False, reason, warnings
            else:
                logger.warning(f"⚠️ POLICY WARNING: {reason}")
                warnings.append(reason)
                
    return True, "", warnings
