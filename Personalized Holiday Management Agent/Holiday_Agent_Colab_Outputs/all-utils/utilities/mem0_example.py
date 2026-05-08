# mem0_example.py
# Demonstrates long-term, evolving user memory for the Holiday Management Agent.
#
# Uses:
#   • ChromaDB (local ./all-utils/db) as the vector store
#   • Groq llama-instant-1.5b as the LLM for memory reasoning
#     (replaces the original OpenAI gpt-4o-mini to avoid OpenAI dependency)
#
# Flow:
#   1. Initialise Memory with Groq + Chroma config
#   2. Store initial preference (e.g. "I prefer beach holidays")
#   3. Update preference (user changes their mind)
#   4. Print observability history — shows the OLD → NEW evolution
#   5. Semantic search — retrieve the most relevant memory

import os

# Remove the SSL cert override that can break Colab network calls
if "SSL_CERT_FILE" in os.environ:
    del os.environ["SSL_CERT_FILE"]

from mem0 import Memory


def get_mem0_config(db_path: str = "all-utils/db") -> dict:
    """
    Build the Mem0 config dict.
    Uses Groq as the LLM provider so no OpenAI key is required.
    """
    return {
        "vector_store": {
            "provider": "chroma",
            "config": {
                "collection_name": "holiday_agent_memory",
                "path": db_path
            }
        },
        "llm": {
            "provider": "groq",
            "config": {
                "model": "llama-3.1-8b-instant",   # fast & cost-effective
                "temperature": 0,                   # deterministic reasoning
                "max_tokens": 256,                  # keep memory calls cheap
                "api_key": os.environ.get("GROQ_API_KEY")
            }
        },
        "embedder": {
            "provider": "huggingface",
            "config": {
                "model": "all-MiniLM-L6-v2"
            }
        }
    }


def run_observability_demo(user_id: str = "traveller_001") -> None:
    """
    End-to-end Mem0 demo: add → update → history → search.
    """

    config = get_mem0_config()
    m = None
    try:
        print("Attempting to initialize Mem0...")
        m = Memory.from_config(config)
        print("Mem0 initialized successfully.")
    except Exception as e:
        print(f"Error initializing Mem0: {e}")
        return # Exit if Mem0 cannot be initialized

    # ── Step 1: Store initial travel preference ───────────────────────────────
    print()
    print("--- [Step 1] Storing Initial Preference ---")
    result = m.add(
        "I prefer beach holidays and warm weather destinations.",
        user_id=user_id
    )

    # Safely extract memory ID (API returns list or dict depending on version)
    mem_id = None
    if isinstance(result, list) and result:
        mem_id = result[0].get("id")
    elif isinstance(result, dict):
        res_list = result.get("results") or result.get("memories") or []
        if res_list:
            mem_id = res_list[0].get("id")
    print(f"   Memory ID captured: {mem_id}")

    # ── Step 2: User changes their mind ──────────────────────────────────────
    print("--- [Step 2] Updating Preference ---")
    m.add(
        "Actually, I have changed my mind. I now prefer mountain hiking and cold weather.",
        user_id=user_id
    )

    # ── Step 3: Observability — show memory evolution ─────────────────────────
    print()
    print("--- [Step 3] Observability Report: Memory Evolution ---")
    if mem_id:
        history = m.history(memory_id=mem_id)
        for entry in history:
            print(f"  Event : {entry.get('event')}")
            old = entry.get('old_memory') or entry.get('old_value') or "(initial)"
            new = entry.get('memory') or entry.get('new_value')
            print(f"  Old   : {old}")
            print(f"  New   : {new}")
            print("  " + "-" * 40)
    else:
        print("  Note: Memory ID not captured — check db folder.")

    # ── Step 4: Semantic search for relevant memories ─────────────────────────
    print()
    print("--- [Step 4] Semantic Memory Search ---")
    search_results = m.search(
        "What kind of holiday destination suits this user?",
        filters={"user_id": user_id}
    )

    memories = (
        search_results.get("results")
        if isinstance(search_results, dict)
        else search_results
    )

    if memories:
        for res in memories:
            val = res.get("memory") or res.get("payload", {}).get("value")
            score = res.get("score", "N/A")
            print(f"  Memory: {val}  (relevance score: {score})")
    else:
        print("  No memories found for this user.")