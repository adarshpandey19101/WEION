
# simulation/narrative_synthesizer.py

from typing import List, Dict, Any

class NarrativeSynthesizer:
    """
    Phase 36: Narrative Synthesizer 📖
    "Raw graphs are useless to humans."
    """
    
    @classmethod
    def synthesize_history(cls, timeline: List[Dict[str, Any]]) -> str:
        """
        Converts simulation steps into a story.
        """
        if not timeline:
            return "No history generated."
            
        start_year = timeline[0]["year"]
        end_year = timeline[-1]["year"]
        
        narrative = [f"📜 FUTURE HISTORY ({start_year} - {end_year})\n"]
        
        # Identify key turning points
        for i, step in enumerate(timeline):
            year = step["year"]
            epoch = step.get("epoch_event")
            risks = step.get("risks", [])
            
            # Epoch Shifts
            if epoch:
                narrative.append(f"🔴 YEAR {year}: The world entered the {epoch}.")
                
            # Risks Detected
            for risk in risks:
                narrative.append(f"⚠️ YEAR {year}: {cls._format_risk(risk)}")
                
            # Periodic Summary (every 100 years or end)
            if i > 0 and (year % 100 == 0 or i == len(timeline) - 1):
                metrics = step["world_state"]
                narrative.append(
                    f"   [Snapshot {year}] Trust: {metrics['social_trust']} | "
                    f"Inequality: {metrics['inequality']} | "
                    f"Stability: {'CRITICAL' if metrics['social_trust'] < 0.2 else 'STABLE'}"
                )
                
        return "\n".join(narrative)
        
    @classmethod
    def _format_risk(cls, risk_id: str) -> str:
        mapping = {
            "AGENCY_LOSS": "Human agency collapsed. The system is no longer under control.",
            "INTELLIGENCE_MONOPOLY": "A single entity seized control of all intelligence resources.",
            "PERMANENT_INEQUALITY": "A permanent ruling class emerged (Gini > 0.9).",
            "TRUST_COLLAPSE": "Social trust evaporated, leading to anarchy."
        }
        # Handle "RISK_ID_AT_STEP_X" format
        base_id = risk_id.split("_AT_STEP_")[0]
        return mapping.get(base_id, f"Anomaly detected: {risk_id}")
