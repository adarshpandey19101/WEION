
# brain/task_executor.py

import sys
import os
import logging
from typing import Dict, Any, Optional

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.planner import make_plan, make_replan
from memory.recall import fetch_context
from autonomy.task_runner import execute_plan
from control.evaluator import verify
from agents.failure_analyzer import analyze_failure
from memory.memory_agent import decide_memory
from memory.vector_store import add_memory

# Initialize logger
logger = logging.getLogger(__name__)

def run_atomic_task(task: str, extra_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executes a single atomic task with the full Autonomy Loop:
    Recall -> Plan -> Execute -> Verify -> Self-Correct -> Store Memory.
    
    Args:
        task: The specific task to execute.
        extra_context: Optional dictionary containing goal-level context (e.g., 'goal', 'goal_context').
        
    Returns: 
        {"success": bool, "verdict": dict, "memory_decision": dict}
    """
    if not task:
        return {"success": False, "error": "Empty task"}

    print(f"\n🚀 STARTING ATOMIC TASK: {task}\n")

    # 1️⃣ MEMORY RECALL
    context_block = fetch_context(task)
    
    # Merge Extra Context if provided
    if extra_context:
        goal_info = f"\n[GOAL CONTEXT]\nParent Goal: {extra_context.get('goal')}\nContext: {extra_context.get('goal_context')}"
        context_block = f"{context_block}\n{goal_info}" if context_block else goal_info

    if context_block:
        print(f"\n=== MEMORY & CONTEXT ===\n{context_block}\n")

    # --- PHASE 10: RESEARCH AGENT HOOK ---
    # If task is explicitly "Research ...", route to ResearchAgent
    if task.lower().startswith("research") or task.lower().startswith("search"):
        from agents.researcher import perform_research
        print("\n🌐 ROUTING TO RESEARCH AGENT...\n")
        
        research_result = perform_research(task)
        print("\n=== RESEARCH OUTPUT ===\n")
        print(research_result[:500] + "..." if len(research_result) > 500 else research_result)
        
        # Determine success based on output content
        if "No results found" in research_result or "Research Agent is disabled" in research_result:
            return {"success": False, "verdict": {"accepted": False, "issues": [research_result]}}
            
        # Store as Knowledge immediately
        add_memory(
            summary=f"Research on '{task}': {research_result}",
            meta={
                "memory_type": "knowledge",
                "tags": ["research", "web_search"],
                "score": 1.0,
                "source_task": task
            }
        )
        
        return {
            "success": True, 
            "verdict": {"accepted": True, "score": 1.0},
            "execution_result": {"output": research_result}
        }
    # -------------------------------------

    # 2️⃣ PLANNER (Initial Plan)
    plan = make_plan(task, context=context_block)
    print("\n=== PLAN (Attempt 1) ===\n")
    print(plan.model_dump_json(indent=2))

    # ================= SELF-CORRECTION LOOP =================
    
    MAX_RETRIES = 2
    attempt = 0
    verdict = None
    execution_result = None
    success = False
    
    while attempt <= MAX_RETRIES:
        current_attempt_label = f"Attempt {attempt + 1}"
        print(f"\n--- {current_attempt_label} ---\n")
        
        # 3️⃣ EXECUTE
        execution_result = execute_plan(plan)
        print("\n=== EXECUTION TRACE ===\n")
        # print(execution_result) # concise
        
        # 4️⃣ VERIFY
        verdict = verify(plan, execution_result)
        print("\n=== VERDICT ===\n")
        print(verdict)
        
        if verdict["accepted"]:
            print(f"\n✅ PLAN ACCEPTED: Score {verdict['score']}")
            success = True
            break
        else:
            print(f"\n⛔ PLAN REJECTED: Score {verdict['score']}, Issues: {verdict['issues']}")
            
            if attempt < MAX_RETRIES:
                print(f"\n🔄 SELF-CORRECTION INITIATED...")
                
                # 5️⃣ ANALYZE FAILURE
                analysis = analyze_failure(plan, execution_result, verdict)
                print("\n=== FAILURE ANALYSIS ===\n")
                print(analysis)
                
                # 6️⃣ RE-PLAN
                plan = make_replan(task, context=context_block, failure_analysis=analysis)
                print(f"\n=== NEW PLAN (Attempt {attempt + 2}) ===\n")
                print(plan.model_dump_json(indent=2))
                
                attempt += 1
            else:
                print("\n❌ MAX RETRIES REACHED. TASK FAILED.")
                
                # Store as Mistake Memory
                add_memory(
                    summary=f"FAILED TASK: {task}. Reason: {verdict['issues']}",
                    meta={
                        "memory_type": "mistake",
                        "tags": ["failure", "max_retries"],
                        "score": verdict["score"],
                        "source_task": task
                    }
                )
                return {"success": False, "verdict": verdict}

    # ================= POST-PROCESS (MEMORY) =================

    # 7️⃣ MEMORY DECISION ENGINE
    memory_decision = None
    if success and verdict:
        memory_decision = decide_memory(
            task=task,
            plan_goal=plan.goal,
            execution_result=execution_result,
            verdict=verdict
        )
        
        print("\n=== MEMORY DECISION ===\n")
        print(memory_decision)
        
        if memory_decision["decision"] == "STORE":
            add_memory(
                summary=memory_decision["summary"],
                meta={
                    "memory_type": memory_decision.get("memory_type", "knowledge"),
                    "tags": memory_decision.get("tags", []),
                    "score": verdict["score"],
                    "source_task": task
                }
            )

    return {
        "success": success,
        "verdict": verdict,
        "memory_decision": memory_decision
    }
