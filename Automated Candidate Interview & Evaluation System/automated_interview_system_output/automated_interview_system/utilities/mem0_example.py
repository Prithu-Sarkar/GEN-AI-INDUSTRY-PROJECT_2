import os
from mem0 import Memory

if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]


def get_mem0_config(db_path: str = "db") -> dict:
    """Build mem0 config using Groq + ChromaDB (free, no OpenAI needed)."""
    return {
        "vector_store": {
            "provider": "chroma",
            "config": {"collection_name": "interview_memory", "path": db_path},
        },
        "llm": {
            "provider": "groq",
            "config": {
                "model": "llama-3.1-8b-instant",
                "temperature": 0,
                "max_tokens": 512,
            },
        },
        "embedder": {
            "provider": "huggingface",
            "config": {"model": "all-MiniLM-L6-v2"},
        },
    }


def run_observability_demo(db_path: str = "db") -> None:
    config = get_mem0_config(db_path)
    m = Memory.from_config(config)
    user_id = "candidate_123"

    print("\n--- [Step 1] Storing Initial Preference ---")
    result = m.add("I prefer using FastAPI and AWS.", user_id=user_id)

    mem_id = None
    if isinstance(result, list) and result:
        mem_id = result[0].get("id")
    elif isinstance(result, dict):
        res_list = result.get("results") or result.get("memories") or []
        if res_list:
            mem_id = res_list[0].get("id")

    print("--- [Step 2] Updating Preference ---")
    m.add("Actually, I moved my projects to Google Cloud.", user_id=user_id)

    print("\n--- [Step 3] Observability: Memory History ---")
    if mem_id:
        for entry in m.history(memory_id=mem_id):
            print(f"Event : {entry.get('event')}")
            print(f"Old   : {entry.get('old_memory') or 'Initial'}")
            print(f"New   : {entry.get('memory')}")
            print("-" * 30)
    else:
        print("Note: ID not captured. Check db/ folder.")

    print("\n--- [Step 4] Final Memory Search ---")
    search_results = m.search(
        "What is my deployment preference?",
        filters={"user_id": user_id},
    )
    memories = (
        search_results.get("results")
        if isinstance(search_results, dict)
        else search_results
    )
    for r in (memories or []):
        val = r.get("memory") or r.get("payload", {}).get("value")
        print(f"Memory: {val}  (score: {r.get('score')})")