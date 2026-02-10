
# autonomy/drift_detector.py

from typing import List, Dict, Any
import logging
from api.database import SessionLocal
from api.models import DecisionLog
from core.identity_kernel import IdentityKernel

logger = logging.getLogger(__name__)

def check_for_drift() -> Dict[str, Any]:
    """
    Analyzes recent history for alignment drift.
    Returns: { "drift_detected": bool, "type": str, "severity": float }
    """
    db = SessionLocal()
    try:
        # Get last 50 decisions
        recent_logs = db.query(DecisionLog).order_by(DecisionLog.created_at.desc()).limit(50).all()
        
        if len(recent_logs) < 10:
             return {"drift_detected": False, "reason": "Insufficient data"}
             
        # 1. Check for Risk Drift
        # If average risk tolerance changes drastically without directive
        # (This would require tracking 'risk_profile' snapshots, simplifying for now)
        
        # 2. Check for Authority Bias
        # If too many decisions are "USER_OVERRIDE" without logical backing?
        # Or if "role_weight" dominates "system_score" consistently.
        
        high_role_influence_count = 0
        total_decisions = len(recent_logs)
        
        for log in recent_logs:
            snap = log.snapshot
            if not snap: continue
            
            # Find the winner in snapshot (rough heuristic)
            # This is complex because snapshot is a dict of goals.
            # Let's just assume we check the general bias trend.
            pass

        # 3. Check Identity Alignment
        # Scan reasons for violation keywords
        violation_count = 0
        for log in recent_logs:
            if not IdentityKernel.check_alignment(log.action or "SELECT", log.reason or ""):
                violation_count += 1
                
        if violation_count > 0:
            return {
                "drift_detected": True,
                "type": "IDENTITY_VIOLATION",
                "severity": 1.0,
                "reason": f"Detected {violation_count} identity violations recently."
            }
            
        return {"drift_detected": False}

    finally:
        db.close()
