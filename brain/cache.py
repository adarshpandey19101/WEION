import hashlib
import json
import os

CACHE_DIR = "logs/llm_cache"
os.makedirs(CACHE_DIR, exist_ok=True)

def _hash(prompt: str) -> str:
    return hashlib.md5(prompt.encode()).hexdigest()

def get_cached(prompt: str):
    path = f"{CACHE_DIR}/{_hash(prompt)}.json"
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)["response"]
    return None

def set_cache(prompt: str, response: str):
    path = f"{CACHE_DIR}/{_hash(prompt)}.json"
    with open(path, "w") as f:
        json.dump({"response": response}, f)
