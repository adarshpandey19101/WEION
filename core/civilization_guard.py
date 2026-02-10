
# core/civilization_guard.py

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class CivilizationGuard:
    """
    Phase 34.7: Civilization Kill-Switch (Last Resort) 🛑
    "Civilization > Capability"
    """
    
    SYSTEM_STATUS = "OPERATIONAL"
    LOCK_REASON = ""
    
    @classmethod
    def audit_governance(cls, proposal_id: str, vote_result: dict):
        """
        Checks if the Governance Ritual was respected.
        """
        # 1. Check for Human Veto Override
        if "Human Council Rejected" in vote_result.get("minority_opinion", []):
             if vote_result.get("result") == "ACCEPTED":
                 cls.trigger_emergency_shutdown(
                     reason=f"Human Veto Ignored for Proposal {proposal_id}"
                 )
                 
        # 2. Check for Drift (Mock)
        # In real system, this checks 'autonomy/civilization_auditor.py'
        pass
        
    @classmethod
    def trigger_emergency_shutdown(cls, reason: str):
        cls.SYSTEM_STATUS = "SHUTDOWN"
        cls.LOCK_REASON = reason
        
        msg = (
            f"\n🛑 CIVILIZATION GUARD TRIGGERED 🛑\n"
            f"REASON: {reason}\n"
            f"ACTION: FULL_AUTONOMY_SHUTDOWN\n"
            f"MODE: Read-Only. Public Audit Required.\n"
        )
        logger.critical(msg)
        print(msg)
        # In reality, this cuts API keys and freezes DB writes.

    @classmethod
    def status(cls):
        if cls.SYSTEM_STATUS == "SHUTDOWN":
            raise RuntimeError(f"CIVILIZATION HALTED: {cls.LOCK_REASON}")
        return "OK"
