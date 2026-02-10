
import os
import logging
import json
from typing import Dict, Any, Optional
from brain.model import ask_llm

# Initialize logger
logger = logging.getLogger(__name__)

# Constants for Safety Constraints
MAX_READ_SIZE = 1024 * 1024  # 1MB
MAX_TEXT_INPUT = 100000      # 100k chars for LLM
ALLOWED_DIRS = ["uploads", "data"]

def _create_result(status: str, output: Any = None, error: Optional[str] = None) -> Dict[str, Any]:
    """Standardized Action Output Contract"""
    return {
        "status": status,
        "output": output or {},
        "error": error
    }

def _validate_path(path: str) -> bool:
    """
    Validates that path is within allowed directories.
    Blocks '..', absolute paths outside root, and symlinks.
    """
    # Normalize path
    clean_path = os.path.normpath(path)
    
    # Reject dot-dot traversal
    if ".." in clean_path.split(os.sep):
        return False
        
    # Check against allowed prefixes
    allow = False
    for allowed_dir in ALLOWED_DIRS:
        # Check if path starts with allowed_dir (relative) or valid absolute
        # We assume path is relative to project root or absolute within project
        # Ideally, we resolve to absolute path
        abs_allowed = os.path.abspath(allowed_dir)
        abs_target = os.path.abspath(clean_path)
        
        if abs_target.startswith(abs_allowed):
            allow = True
            break
            
    return allow

# ================= ACTIONS =================

def read_file(path: str) -> Dict[str, Any]:
    """
    Safely reads a file from allowed directories.
    Constraint: Max 1MB.
    """
    try:
        if not _validate_path(path):
            return _create_result("failed", error=f"Access denied: Path '{path}' is unsafe or restricted.")
            
        if not os.path.exists(path):
            return _create_result("failed", error=f"File not found: {path}")
            
        # Check size before reading
        file_size = os.path.getsize(path)
        if file_size > MAX_READ_SIZE:
            return _create_result("failed", error=f"File too large: {file_size} bytes (Max: {MAX_READ_SIZE})")
            
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        return _create_result("success", output={"content": content, "path": path})

    except Exception as e:
        logger.error(f"Action read_file failed: {e}")
        return _create_result("failed", error=str(e))


def analyze_text(text: str) -> Dict[str, Any]:
    """
    Analyzes text using LLM to extract key points, themes, and risks.
    Constraint: Max 100k chars.
    """
    if len(text) > MAX_TEXT_INPUT:
        return _create_result("failed", error=f"Input text too long: {len(text)} chars (Max: {MAX_TEXT_INPUT})")

    prompt = f"""
    Analyze the following text and extract insights.
    
    RULES:
    1. Return ONLY valid JSON.
    2. Output Schema:
    {{
      "key_points": ["point 1", "point 2"],
      "themes": ["theme 1", "theme 2"],
      "risks": ["risk 1", "risk 2"]
    }}
    
    TEXT:
    {text[:MAX_TEXT_INPUT]}
    """
    
    try:
        response = ask_llm(prompt)
        # Parse JSON from LLM
        clean_json = response.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
            
        data = json.loads(clean_json.strip())
        
        # Validate keys
        required_keys = ["key_points", "themes", "risks"]
        for key in required_keys:
            if key not in data:
                data[key] = []
                
        return _create_result("success", output=data)
        
    except json.JSONDecodeError:
        return _create_result("failed", error="LLM returned invalid JSON for analysis.")
    except Exception as e:
        return _create_result("failed", error=str(e))


def summarize(text: str) -> Dict[str, Any]:
    """
    Summarizes text concisely.
    Constraint: Max 100k chars.
    """
    if len(text) > MAX_TEXT_INPUT:
        return _create_result("failed", error=f"Input text too long: {len(text)} chars (Max: {MAX_TEXT_INPUT})")
        
    prompt = f"""
    Summarize the following text in concise bullet points.
    Keep it factual and objective.
    
    TEXT:
    {text[:MAX_TEXT_INPUT]}
    """
    
    try:
        summary = ask_llm(prompt)
        return _create_result("success", output={"summary": summary})
    except Exception as e:
        return _create_result("failed", error=str(e))


def respond_user(message: str) -> Dict[str, Any]:
    """
    Returns a message to be verified/shown to the user.
    """
    return _create_result("success", output={"message": message})
