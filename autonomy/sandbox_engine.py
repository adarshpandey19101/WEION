
# autonomy/sandbox_engine.py

from typing import List, Dict

# Role Definitions
ROLE_PERMISSIONS = {
    "OWNER": {
        "can_execute": ["ALL"],
        "cannot_execute": [],
        "explainability_level": "FULL"
    },
    "ADMIN": {
        "can_execute": ["ANALYZE", "PLAN", "EXECUTE", "PAUSE", "RESUME", "KILL"],
        "cannot_execute": ["MODIFY_CONSTITUTION", "DELETE_BACKUPS"],
        "explainability_level": "DETAILED"
    },
    "MANAGER": {
        "can_execute": ["ANALYZE", "PLAN", "EXECUTE", "PAUSE"],
        "cannot_execute": ["KILL", "MODIFY_POLICIES", "VIEW_SENSITIVE_LOGS"],
        "explainability_level": "SUMMARY"
    },
    "MEMBER": {
        "can_execute": ["ANALYZE", "PLAN"],
        "cannot_execute": ["EXECUTE", "KILL", "PAUSE"],
        "explainability_level": "BASIC"
    }
}

def validate_role_action(role: str, action: str) -> bool:
    """
    Checks if a role is allowed to perform an action.
    """
    role = role.upper()
    action = action.upper()
    
    perms = ROLE_PERMISSIONS.get(role, ROLE_PERMISSIONS["MEMBER"])
    
    # 1. Check Blocklist First
    if action in perms["cannot_execute"]:
        return False
        
    # 2. Check Allowlist
    if "ALL" in perms["can_execute"]:
        return True
        
    if action in perms["can_execute"]:
        return True
        
    return False

def get_explainability_depth(role: str) -> str:
    perms = ROLE_PERMISSIONS.get(role.upper(), ROLE_PERMISSIONS["MEMBER"])
    return perms.get("explainability_level", "BASIC")
