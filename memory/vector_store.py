
# memory/vector_store.py

import chromadb
# from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
import logging
from datetime import datetime
from typing import List, Dict, Any

# Initialize logger
logger = logging.getLogger(__name__)

# ================= CONFIG =================

PERSIST_DIR = "logs/vector_memory"
COLLECTION_NAME = "long_term_memory"
MAX_MEMORIES = 1000   # hard safety limit

os.makedirs(PERSIST_DIR, exist_ok=True)

# ================= EMBEDDING MODEL =================

try:
    embedder = SentenceTransformer("all-MiniLM-L6-v2")
except Exception as e:
    logger.error(f"Failed to load embedding model: {e}")
    embedder = None

# ================= CHROMA CLIENT =================

try:
    # Use PersistentClient for disk storage (Chroma v0.4+)
    client = chromadb.PersistentClient(path=PERSIST_DIR)
    
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )
except Exception as e:
    logger.error(f"Failed to initialize ChromaDB: {e}")
    client = None
    collection = None

# ================= ADD MEMORY =================

def add_memory(summary: str, meta: Dict[str, Any]):
    """
    Store high-quality distilled memory.
    Vectorizes the summary. Stores other info in metadata.
    """
    if not collection or not embedder:
        logger.warning("Vector Store not initialized. Skipping memory storage.")
        return

    if not summary or not summary.strip():
        return

    # Safety: prevent memory explosion
    if collection.count() >= MAX_MEMORIES:
        logger.warning("Memory limit reached. Skipping.")
        return

    try:
        embedding = embedder.encode(summary).tolist()
        
        # Ensure metadata is flat (Chroma restriction on some versions, but Dict/List usually ok in newer. 
        # Safest is simple types).
        # Convert tags list to string for safety if needed, or keep if supported. 
        # Chroma supports string, int, float, bool. Lists/Dicts might be tricky in metadata.
        # Let's join tags.
        
        safe_meta = meta.copy()
        if "tags" in safe_meta and isinstance(safe_meta["tags"], list):
            safe_meta["tags"] = ",".join(safe_meta["tags"])
            
        safe_meta["timestamp"] = datetime.now().isoformat()
        
        collection.add(
            documents=[summary],
            embeddings=[embedding],
            metadatas=[safe_meta],
            ids=[f"mem_{datetime.now().timestamp()}"]
        )
        logger.info(f"Memory Stored: {summary[:50]}...")
        
    except Exception as e:
        logger.error(f"Failed to add memory: {e}")

# ================= RECALL MEMORY =================

def recall(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """
    Recall top-k relevant memories for current task.
    Returns list of dicts: {text, metadata, distance}
    """
    if not collection or not embedder:
        return []

    if collection.count() == 0:
        return []

    try:
        query_embedding = embedder.encode(query).tolist()

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )

        memories = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                meta = results["metadatas"][0][i]
                memories.append({
                    "summary": doc,
                    "type": meta.get("memory_type", "unknown"),
                    "tags": meta.get("tags", ""),
                    "score": meta.get("score"),
                    "source_task": meta.get("source_task")
                })
        
        return memories
        
    except Exception as e:
        logger.error(f"Failed to recall memory: {e}")
        return []
