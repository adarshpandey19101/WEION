import subprocess
from api.config import OLLAMA_MODEL, OLLAMA_TIMEOUT


def run_llm(prompt: str) -> str:
    try:
        result = subprocess.run(
            ["ollama", "run", OLLAMA_MODEL],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=OLLAMA_TIMEOUT
        )

        if result.returncode != 0:
            return f"Ollama error: {result.stderr}"

        return result.stdout.strip()

    except Exception as e:
        return f"Ollama exception: {str(e)}"
