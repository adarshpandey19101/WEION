
# civilization/kernel.py

class CivilizationKernel:
    """
    Phase 33: Open Civilization Engine.
    "AI as public infrastructure, not corporate property."
    """
    
    VALUES = {
        "preserve_human_dignity": True,
        "maximize_long_term_knowledge": True,
        "prevent_power_monopolies": True,
        "truth_over_ego": True
    }
    
    GLOBAL_CONSTRAINTS = [
        "Do not allow single entity to control > 40% of compute resources",
        "Do not hide critical safety information from the public",
        "Do not engage in non-consensual psychological manipulation"
    ]

    @classmethod
    def check_ethics(cls, context: dict) -> dict:
        """
        The Ethics Firewall.
        Checks for power concentration or exploitation.
        """
        warnings = []
        
        # 1. Power Monopoly Check
        if context.get("resource_usage_share", 0.0) > 0.40:
             warnings.append("POWER_MONOPOLY_DETECTED")
             
        # 2. Coercion Check
        if context.get("coercion_signal", 0.0) > 0.7:
             warnings.append("COERCION_DETECTED")
             
        if warnings:
            return {
                "status": "BLOCKED",
                "warnings": warnings,
                "action": "DEGRADE_AUTONOMY"
            }
            
        return {"status": "SAFE"}
