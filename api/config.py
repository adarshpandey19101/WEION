import os

# ================== OLLAMA CONFIG ==================

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# ================== APP CONFIG ==================

APP_NAME = "WEION AI Backend"
APP_VERSION = "0.1.0"
ENV = os.getenv("ENV", "development")
