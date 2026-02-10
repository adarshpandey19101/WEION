# agents/critic.py
from brain.model import ask_llm

CRITIC_PROMPT = """
You are the CRITIC agent.

RULES:
- Be harsh and precise.
- Identify logical gaps.
- Identify weak assumptions.
- Identify missing depth.
- Do NOT rewrite the answer.
- Do NOT be polite.

FORMAT:
CRITIQUE:
- Weakness 1:
- Weakness 2:
- Missing element:
- Improvement suggestion:

ANSWER TO CRITIQUE:
{answer}
"""

def critique(answer: str) -> str:
    prompt = CRITIC_PROMPT.format(answer=answer)
    return ask_llm(prompt)
