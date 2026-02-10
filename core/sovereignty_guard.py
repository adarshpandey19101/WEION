
# core/sovereignty_guard.py

import logging
import sys
from datetime import datetime

logger = logging.getLogger(__name__)

class SovereigntyGuard:
    """
    The Final Barrier.
    If this is triggered, WEION halts to prevent irreversible damage.
    """
    
    SYSTEM_LOCKED = False
    LOCK_REASON = ""
    
    @classmethod
    def emergency_halt(cls, reason: str, severity: float):
        """
        Triggers the Kill Switch.
        """
        cls.SYSTEM_LOCKED = True
        cls.LOCK_REASON = reason
        
        message = (
            f"\n🚨 SOVEREIGNTY GUARD TRIGGERED 🚨\n"
            f"REASON: {reason}\n"
            f"SEVERITY: {severity}\n"
            f"ACTION: System Halted. Manual Governance Required.\n"
        )
        logger.critical(message)
        print(message)
        
        # In a real system, this might exit the process or freeze all API endpoints.
        # For simulation/test, we set the flag.
        
    @classmethod
    def check_status(cls):
        if cls.SYSTEM_LOCKED:
            raise RuntimeError(f"SYSTEM LOCKED BY SOVEREIGNTY GUARD: {cls.LOCK_REASON}")
            
    # Phase 31.6: Immutable Memory Log (Simulated)
    @classmethod
    def log_identity_event(cls, event_type: str, details: str):
        # Write-once log
        entry = f"[{datetime.utcnow()}] IDENTITY_EVENT: {event_type} - {details}\n"
        try:
            with open("logs/identity_ledger.log", "a") as f:
                f.write(entry)
        except Exception:
            pass
