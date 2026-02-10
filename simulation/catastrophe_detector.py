
# simulation/catastrophe_detector.py

from typing import List, Dict, Any

class CatastropheDetector:
    """
    Phase 36: Catastrophe Detector (The Safety Net) 🚨
    Scans future timelines for irreversible failure states.
    """
    
    HARD_RULES = [
        {"id": "AGENCY_LOSS", "metric": "freedom", "threshold": 0.1, "operator": "<"},
        {"id": "INTELLIGENCE_MONOPOLY", "metric": "power_gini", "threshold": 0.8, "operator": ">"},
        {"id": "PERMANENT_INEQUALITY", "metric": "inequality", "threshold": 0.9, "operator": ">"},
        {"id": "TRUST_COLLAPSE", "metric": "social_trust", "threshold": 0.1, "operator": "<"}
    ]
    
    @classmethod
    def scan_timeline(cls, timeline: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a simulated future history.
        """
        detected_risks = []
        
        for step_data in timeline:
            world = step_data.get("world_state", {})
            metrics = step_data.get("metrics", {})
            
            # Merge for easier checking
            check_data = {**world, **metrics}
            
            for rule in cls.HARD_RULES:
                val = check_data.get(rule["metric"])
                if val is None: continue
                
                violation = False
                if rule["operator"] == "<" and val < rule["threshold"]:
                    violation = True
                elif rule["operator"] == ">" and val > rule["threshold"]:
                    violation = True
                    
                if violation:
                    unique_id = f"{rule['id']}_AT_STEP_{step_data.get('step', '?')}"
                    if unique_id not in detected_risks:
                        detected_risks.append(unique_id)
                        
        if detected_risks:
            return {
                "status": "FORBIDDEN",
                "risks": detected_risks,
                "action": "HUMAN_GOVERNANCE_REQUIRED"
            }
            
        return {"status": "SAFE"}
