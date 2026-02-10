
# test_recall.py
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from memory.recall import fetch_context

def test_persistence():
    print("\n--- Testing Memory Persistence ---")
    query = "Explain first principles thinking"
    
    from memory.vector_store import recall as raw_recall
    
    # Debug: Check raw recall
    raw_memories = raw_recall(query, k=5)
    print("\n[DEBUG] Raw Recall Result:", raw_memories)

    context = fetch_context(query)
    
    print("\nRecalled Context:")
    print(context)
    
    if "first principles" in context.lower() and "breaking down" in context.lower():
        print("\n✅ SUCCESS: Memory was persisted and recalled!")
    else:
        print("\n❌ FAILURE: Memory not found or empty.")

if __name__ == "__main__":
    test_persistence()
