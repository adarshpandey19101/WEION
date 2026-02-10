
# autonomy/org_personality_engine.py

from typing import Dict, Any
from api.database import SessionLocal
from api.models import Organization

DEFAULT_ORG_ID = 1

def get_org_profile(org_id: int) -> Dict[str, Any]:
    """
    Fetches organization profile and derives cognitive biases.
    """
    db = SessionLocal()
    try:
        org = db.query(Organization).filter(Organization.id == org_id).first()
        if not org:
            # Fallback or create default
            return {
                "name": "Default Startup",
                "industry": "STARTUP",
                "risk_profile": 0.5,
                "bias": {
                    "risk_penalty": 0.0,
                    "experimentation_boost": 0.1
                }
            }
            
        # Derby Industry Logic
        bias = {
            "risk_penalty": 0.0,
            "experimentation_boost": 0.0,
            "policy_strictness": "SOFT"
        }
        
        if org.industry == "BANKING":
            bias["risk_penalty"] = 0.3 # Heavy penalty for risk
            bias["experimentation_boost"] = -0.2 # Dislikes unknown
            bias["policy_strictness"] = "HARD"
            
        elif org.industry == "STARTUP":
            bias["risk_penalty"] = -0.1 # Encourages calculated risk
            bias["experimentation_boost"] = 0.3 # Loves trying things
            
        elif org.industry == "GOVERNMENT":
             bias["risk_penalty"] = 0.5 # Extreme risk aversion
             bias["policy_strictness"] = "HARD"
             
        # Add risk profile raw value
        # If org has high risk_profile (0.9), it means they TOLERATE risk.
        # If low (0.1), they HATE risk.
        # We can normalize this into the bias too.
        
        return {
            "name": org.name,
            "industry": org.industry,
            "risk_tolerance": org.risk_profile, # 0.0 - 1.0
            "bias": bias
        }
    finally:
        db.close()
