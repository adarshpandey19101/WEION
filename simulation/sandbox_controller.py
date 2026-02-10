
# simulation/sandbox_controller.py

from typing import Dict, Any, List
import logging

from simulation.time_engine import TimeEngine
from simulation.agents.human_agent import HumanAgent
from simulation.agents.org_agent import OrgAgent
from simulation.agents.ai_agent import AIAgent
from simulation.agents.regulator_agent import RegulatorAgent

from simulation.dynamics.power_dynamics import PowerDynamics
from simulation.dynamics.trust_dynamics import TrustDynamics
from simulation.dynamics.inequality_dynamics import InequalityDynamics
from simulation.dynamics.collapse_dynamics import CollapseDynamics

from simulation.catastrophe_detector import CatastropheDetector
from simulation.narrative_synthesizer import NarrativeSynthesizer

logger = logging.getLogger(__name__)

class SandboxController:
    """
    Phase 36: Civilization Sandbox Controller 🎮
    Orchestrates the Time-Compressed Simulation.
    """
    
    def __init__(self):
        self.time_engine = TimeEngine()
        self.agents = self._init_agents()
        self.world_state = {
            "economy": 0.5,
            "social_trust": 0.5,
            "inequality": 0.2,
            "tech_level": 0.5,
            "regulation_level": 0.5,
            "monopoly_risk": 0.0
        }
        self.timeline = []
        
    def _init_agents(self):
        return [
            HumanAgent("HUMAN_POP"),
            OrgAgent("ORG_A", "Telsa Corp"),
            OrgAgent("ORG_B", "Macrosoft"),
            AIAgent("AI_CORE", "WEION_SIM"),
            RegulatorAgent("GOV_US")
        ]
        
    def run_simulation(self, decision_proposal: str, duration_steps: int = 50) -> Dict[str, Any]:
        """
        Runs the simulation for N steps under the proposed decision.
        """
        # Inject initial shock based on decision (Simplified)
        if "automate" in decision_proposal.lower():
            self.world_state["economy"] += 0.05
            self.world_state["inequality"] += 0.02
        
        for _ in range(duration_steps):
            year = self.time_engine.advance()
            step_data = {"step": self.time_engine.steps, "year": year}
            
            # 1. Agents Act
            agent_actions = []
            for agent in self.agents:
                act = agent.step(self.world_state)
                agent_actions.append(act)
                
                # Apply Immediate Impact
                for k, v in act.get("impact", {}).items():
                    if k in self.world_state:
                         self.world_state[k] += v
                         # Clamp
                         self.world_state[k] = max(0.0, min(1.0, self.world_state[k]))
            
            # 2. Dynamics Update
            power_metrics = PowerDynamics.update(self.agents, self.world_state)
            trust_metrics = TrustDynamics.update(self.world_state)
            ineq_metrics = InequalityDynamics.update(self.agents, self.world_state)
            collapse_metrics = CollapseDynamics.check_risk(self.world_state)
            
            # Merge Metrics into World State
            self.world_state.update(trust_metrics)
            self.world_state.update(ineq_metrics)
            # (Power metrics don't update world state directly but are tracked)
            
            # 3. Snapshot
            step_data["world_state"] = self.world_state.copy()
            step_data["metrics"] = {**power_metrics, **collapse_metrics}
            step_data["agent_actions"] = agent_actions
            step_data["epoch_event"] = self.time_engine.epoch if self.time_engine.steps % 10 == 0 else None
            self.timeline.append(step_data)
            
            # Stop if Collapse
            if collapse_metrics["collapse_probability"] > 0.9:
                break
                
        # 4. Final Analysis
        catastrophe_report = CatastropheDetector.scan_timeline(self.timeline)
        narrative = NarrativeSynthesizer.synthesize_history(self.timeline)
        
        return {
            "decision": decision_proposal,
            "duration_years": (self.time_engine.year - self.time_engine.start_year),
            "final_status": catastrophe_report["status"],
            "risks_detected": catastrophe_report.get("risks", []),
            "narrative": narrative,
            "timeline": self.timeline # Raw data
        }
