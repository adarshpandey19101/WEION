
# test_product_brain.py
import sys
import os
from unittest.mock import patch

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from api.database import SessionLocal, engine, Base
from api.models import (
    UserCommunicationStyle, OrgPolicy, UsageLog
)
from autonomy.communication_engine import apply_communication_style
from autonomy.policy_engine import check_policy_compliance
from autonomy.usage_monitor import log_usage

# Ensure DB tables exist for test
Base.metadata.create_all(bind=engine)

def reset_db(db):
    db.query(UserCommunicationStyle).delete()
    db.query(OrgPolicy).delete()
    db.query(UsageLog).delete()
    db.commit()

def test_product_brain():
    print("\n--- Test: Productization & Org Brain (Phases 22-24) ---")
    db = SessionLocal()
    try:
        reset_db(db)
        
        # -------------------------------------------------------------
        # Phase 22: Communication Intelligence
        # -------------------------------------------------------------
        print("\n[Phase 22] Testing Communication Modulation...")
        user_id = "talkative_user"
        style = UserCommunicationStyle(
            user_id=user_id,
            tone="blunt",
            assertiveness=0.9
        )
        db.add(style)
        db.commit()
        
        raw_text = "I think maybe we should launch the product. I recommend that you check the logs."
        mod_text = apply_communication_style(raw_text, user_id)
        
        print(f"Raw: {raw_text}")
        print(f"Mod: {mod_text}")
        
        # Assertions
        assert "I think" not in mod_text
        assert "Action required:" in mod_text
        assert "Do this:" in mod_text
        
        # -------------------------------------------------------------
        # Phase 23: Org Policy
        # -------------------------------------------------------------
        print("\n[Phase 23] Testing Policy Enforcement...")
        policy = OrgPolicy(
            category="SECURITY",
            rule="public_upload", # Keyword to ban
            severity="HARD",
            active=True
        )
        db.add(policy)
        db.commit()
        
        # Attempt Violation
        action = "Initiating public_upload of credentials"
        allowed, reason, warnings = check_policy_compliance(action)
        
        print(f"Action: {action}")
        print(f"Allowed: {allowed}")
        print(f"Reason: {reason}")
        
        assert allowed is False
        assert "SECURITY" in reason
        
        # Attempt Safety
        action_safe = "Internal backup"
        allowed_safe, _, _ = check_policy_compliance(action_safe)
        assert allowed_safe is True

        # -------------------------------------------------------------
        # Phase 24: Usage Log
        # -------------------------------------------------------------
        print("\n[Phase 24] Testing Usage Monitoring...")
        log_usage(user_id, "decision", tokens=100)
        
        log_entry = db.query(UsageLog).first()
        print(f"Logged: {log_entry.action} Cost: ${log_entry.cost}")
        
        assert log_entry.action == "decision"
        assert log_entry.cost > 0

        print("\n✅ Product Brain Verified!")

    finally:
        db.close()

if __name__ == "__main__":
    test_product_brain()
