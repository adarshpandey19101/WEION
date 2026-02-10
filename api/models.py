from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime, JSON, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from api.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    context = Column(Text) # Additional implementation details
    org_id = Column(Integer, default=1) # Phase 29: Org Isolation
    tasks = Column(JSON, default=[])  # Stored as JSON array
    timestamp = Column(String, default=lambda: datetime.now().isoformat())

class Goal(Base):
    __tablename__ = "goals"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    status = Column(String, default="not-started")
    priority = Column(String, default="medium")
    progress = Column(Integer, default=0)
    deadline = Column(String, nullable=True)
    createdAt = Column(String, default=lambda: datetime.now().isoformat())

# Phase 7: Goal Persistence Models

class GoalExecution(Base):
    __tablename__ = "goal_executions"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, default=1) # Phase 29: Org Isolation
    objective = Column(Text, nullable=False)
    context = Column(Text)
    status = Column(String, default="PENDING")  # PENDING, RUNNING, COMPLETED, FAILED, PAUSED
    tasks = Column(JSON)          # List[str]
    current_task_index = Column(Integer, default=0)
    results = Column(JSON)        # Atomic execution traces
    error = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AtomicTaskCheckpoint(Base):
    __tablename__ = "atomic_task_checkpoints"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goal_executions.id"))
    task_index = Column(Integer)
    task_text = Column(Text)
    verdict = Column(JSON)
    execution_result = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    status = Column(String, default="pending")
    confidence = Column(Float, default=0.0)
    startTime = Column(String, default=lambda: datetime.now().isoformat())
    endTime = Column(String, nullable=True)
    subtasks = Column(JSON, default=[])

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())
    level = Column(String)
    message = Column(String)

class Setting(Base):
    __tablename__ = "settings"

    key = Column(String, primary_key=True, index=True)
    value = Column(JSON)  # Store value as JSON to handle diff types

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(String, primary_key=True, index=True)
    type = Column(String)
    title = Column(String)
    message = Column(String)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())
    read = Column(Boolean, default=False)

class PlannerLog(Base):
    __tablename__ = "planner_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(String)
    parsed_plan = Column(JSON, nullable=True)
    raw_output = Column(String)
    confidence = Column(Float)
    timestamp = Column(String, default=lambda: datetime.now().isoformat())
    successful = Column(Boolean)
    error_reason = Column(String, nullable=True)
    planner_version = Column(String, default="v1.0")

class VerdictLog(Base):
    __tablename__ = "verdict_logs"

    id = Column(Integer, primary_key=True, index=True)
    planner_log_id = Column(Integer, ForeignKey("planner_logs.id"))
    score = Column(Float)
    accepted = Column(Boolean)
# Phase 8: Goal Arbitration Models

class GoalPriority(Base):
    __tablename__ = "goal_priorities"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer, ForeignKey("goal_executions.id"), unique=True)
    org_id = Column(Integer, default=1)
    
    impact = Column(Float, default=0.5)      # 0-1 (Business / Outcome Impact)
    urgency = Column(Float, default=0.5)     # 0-1 (Time Sensitivity)
    effort = Column(Float, default=0.5)      # 0-1 (Higher = harder)
    risk = Column(Float, default=0.1)        # 0-1 (Failure Probability)
    confidence = Column(Float, default=0.5)  # 0-1 (System confidence)
    
    score = Column(Float, default=0.0)       # Final computed score
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DecisionLog(Base):
    __tablename__ = "decision_logs"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, default=1)
    decision_type = Column(String)  # SELECT | PAUSE | KILL
    selected_goal_id = Column(Integer, nullable=True)
    affected_goals = Column(JSON)   # List of paused/killed goal IDs
    reason = Column(Text)
    confidence = Column(Float)
    snapshot = Column(JSON)         # all goal scores at decision time
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionOutcome(Base):
    __tablename__ = "decision_outcomes"

    id = Column(Integer, primary_key=True, index=True)
    decision_log_id = Column(Integer, ForeignKey("decision_logs.id"))
    goal_id = Column(Integer, ForeignKey("goal_executions.id"))
    
    outcome = Column(String)  # SUCCESS | FAILURE | PARTIAL | KILLED | PAUSED_TOO_LONG
    duration = Column(Float)      # seconds
    retries = Column(Integer)
    final_score = Column(Float)   # verifier score
    user_feedback = Column(Float, nullable=True)  # optional (0-1)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class PriorityWeights(Base):
    __tablename__ = "priority_weights"

    id = Column(Integer, primary_key=True, index=True)
    impact = Column(Float, default=0.4)
    urgency = Column(Float, default=0.3)
    confidence = Column(Float, default=0.2)
    effort = Column(Float, default=0.1)
    risk = Column(Float, default=0.2)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserPreference(Base):
    __tablename__ = "user_preferences"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, default="default_user")
    
    # 0.0 = Quality/Safe/Stable, 1.0 = Speed/Risky/Experimental
    pref_speed_vs_quality = Column(Float, default=0.5) 
    pref_risk_tolerance = Column(Float, default=0.5)
    pref_experimentation = Column(Float, default=0.5)
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class UserBehaviorSignal(Base):
    __tablename__ = "user_behavior_signals"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, default=1)
    user_id = Column(String, default="default_user")
    
    signal_type = Column(String) # GOAL_KILLED, GOAL_PAUSED, GOAL_COMPLETED_FAST, GOAL_RETRIED
    goal_id = Column(Integer)
    signal_metadata = Column(JSON)
    
    created_at = Column(DateTime, default=datetime.utcnow)

class UserRole(Base):
    __tablename__ = "user_roles"


    user_id = Column(String, primary_key=True)
    role = Column(String, default="OWNER") # OWNER, ADMIN, MANAGER, CONTRIBUTOR

class UserCommunicationStyle(Base):
    __tablename__ = "user_communication_style"

    user_id = Column(String, primary_key=True)
    tone = Column(String, default="professional")  # calm, direct, motivational, blunt
    verbosity = Column(String, default="medium")   # short, medium, detailed
    assertiveness = Column(Float, default=0.5)     # 0.0-1.0
    empathy = Column(Float, default=0.5)           # 0.0-1.0
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class OrgPolicy(Base):
    __tablename__ = "org_policies"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, default=1)
    category = Column(String)   # SECURITY, LEGAL, BUDGET
    rule = Column(Text)
    severity = Column(String)   # HARD / SOFT
    active = Column(Boolean, default=True)

class UsageLog(Base):
    __tablename__ = "usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    action = Column(String)     # goal_run, decision, llm_call
    tokens = Column(Integer, default=0)
    cost = Column(Float, default=0.0)
    timestamp = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String) # GOAL / TASK / DECISION
    entity_id = Column(Integer)
    action = Column(String)      # SELECT / PAUSE / KILL / EXECUTE
    reason = Column(Text)
    policy_checks = Column(JSON)      # passed / warnings / blocks
    scores_snapshot = Column(JSON)    # impact, urgency, user_pref, role, personality
    created_at = Column(DateTime, default=datetime.utcnow)

class DecisionTrace(Base):
    __tablename__ = "decision_traces"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer)
    step = Column(String)        # PLANNING / EXECUTION / VERIFICATION / ARBITRATION
    input_snapshot = Column(JSON)
    output_snapshot = Column(JSON)
    confidence = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class EmotionalMemory(Base):
    __tablename__ = "emotional_memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    emotion = Column(String)          # STRESSED / CONFIDENT / FRUSTRATED / CALM
    trigger_event = Column(String)    # GOAL_FAILED / DEADLINE / USER_OVERRIDE
    intensity = Column(Float)         # 0.0 - 1.0
    context = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class TrustSnapshot(Base):
    __tablename__ = "trust_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    goal_id = Column(Integer)
    decision_type = Column(String)  # SELECT / PAUSE / KILL
    final_score = Column(Float)
    factor_breakdown = Column(JSON)
    policy_flags = Column(JSON)
    emotion_state = Column(String)
    user_preference_bias = Column(JSON)
    personality_mode = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    industry = Column(String)
    default_personality = Column(String)  # CEO / CTO / Researcher
    risk_profile = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserOrganization(Base):
    __tablename__ = "user_organizations"

    user_id = Column(String, primary_key=True)
    org_id = Column(Integer, primary_key=True)
    role = Column(String)  # OWNER / ADMIN / MEMBER

class EvolutionDirective(Base):
    __tablename__ = "evolution_directives"

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, default=1)
    source = Column(String)       # META / FAILURE / HUMAN
    change_type = Column(String)  # WEIGHT_SHIFT / RULE_TIGHTEN / GOAL_SUPPRESS
    reason = Column(Text)
    risk_level = Column(Float)
    applied_at = Column(DateTime, default=datetime.utcnow)

class ResponsibilityChain(Base):
    """
    Phase 32: Liability & Blame Routing.
    Tracks the full chain of custody for a decision.
    """
    __tablename__ = "responsibility_chain"
    
    id = Column(Integer, primary_key=True, index=True)
    decision_id = Column(String, index=True) # Linked to DecisionLog
    goal_id = Column(Integer)
    
    who_suggested = Column(String)  # Agent Module Name
    who_approved = Column(String)   # User ID or "AUTO_SYSTEM"
    who_executed = Column(String)   # Execution Agent ID
    
    policy_snapshot = Column(JSON)  # What policies allowed this?
    risk_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

class GovernanceVote(Base):
    """
    Phase 34: Governance Power Distribution.
    Tracks votes from the 4 councils.
    """
    __tablename__ = "governance_votes"
    
    id = Column(Integer, primary_key=True, index=True)
    proposal_id = Column(String, index=True)
    
    # Vote Breakdown
    human_vote = Column(String)     # YES / NO / VETO
    technical_vote = Column(String) # YES / NO
    economic_vote = Column(String)  # YES / NO
    ai_vote = Column(String)        # YES / NO
    
    result = Column(String)         # ACCEPTED / REJECTED
    reason = Column(Text)
    minority_opinion = Column(JSON) # List of dissenting reasons
    timestamp = Column(DateTime, default=datetime.utcnow)
