
import os
from mem0 import Memory


def run_observability_demo():
    """
    Demonstrate Mem0 add / update / history / search using:
      - vector store : ChromaDB (local)
      - LLM          : Groq  llama-3.1-8b-instant  (free tier)
    """
    # Remove any stale SSL env var that breaks ChromaDB on some runtimes.
    os.environ.pop("SSL_CERT_FILE", None)

    config = {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "storyforge_demo",
                "path": "storyforge_agent/outputs/mem0_db",
            },
        },
        "llm": {
            "provider": "groq",
            "config": {
                "model": "llama-3.1-8b-instant",
                "temperature": 0,
                "groq_api_key": os.environ.get("GROQ_API_KEY"),
            },
        },
        "embedder": {
            "provider": "huggingface",
            "config": {"model": "multi-qa-MiniLM-L6-cos-v1"},
        },
    }

    m = Memory.from_config(config)
    user_id = "storyforge_user_001"

    print("
--- [1] Storing initial preference ---")
    result = m.add("I prefer using FastAPI and AWS.", user_id=user_id)

    # Robustly extract the memory ID regardless of result shape.
    mem_id = None
    if isinstance(result, list) and result:
        mem_id = result[0].get("id")
    elif isinstance(result, dict):
        for key in ("results", "memories"):
            lst = result.get(key, [])
            if lst:
                mem_id = lst[0].get("id")
                break

    print("--- [2] Updating preference ---")
    m.add("Actually, I moved my projects to Google Cloud.", user_id=user_id)

    print("
--- [3] Memory history ---")
    if mem_id:
        for entry in m.history(memory_id=mem_id):
            old = entry.get("old_memory") or entry.get("old_value") or "Initial"
            new = entry.get("memory") or entry.get("new_value")
            print(f"  Event: {entry.get('event')}  |  {old!r} → {new!r}")
    else:
        print("  (ID not captured — check outputs/mem0_db/)")

    print("
--- [4] Search final state ---")
    sr = m.search("What is my deployment preference?", filters={"user_id": user_id})
    memories = sr.get("results") if isinstance(sr, dict) else sr
    for r in (memories or []):
        val = r.get("memory") or r.get("payload", {}).get("value")
        print(f"  Memory: {val!r}  (score={r.get('score')})")
