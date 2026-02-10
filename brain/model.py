import subprocess
from brain.cache import get_cached, set_cache

MODEL = "qwen2.5:7b"

def ask_llm(prompt: str) -> str:
    cached = get_cached(prompt)
    if cached:
        return cached

    result = subprocess.run(
        ["ollama", "run", MODEL, prompt],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    set_cache(prompt, output)
    return output
