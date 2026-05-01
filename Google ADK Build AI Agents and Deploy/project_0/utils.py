"""
Utility helpers for the Reading List Curator.
Unchanged from course — ANSI colours work in Colab terminals too.
"""
from google.genai import types


class Colors:
    RESET   = "\033[0m";  BOLD    = "\033[1m"
    BLACK   = "\033[30m"; CYAN    = "\033[36m"; GREEN  = "\033[32m"
    BG_BLUE = "\033[44m"; BG_GREEN= "\033[42m"; BG_RED = "\033[41m"


async def display_state_async(session_service, app_name, user_id, session_id, label="State"):
    """Pretty-print current session state."""
    try:
        session = await session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_id
        )
        st = session.state or {}
        print(f"\n{'-'*12} {label} {'-'*12}")
        print(f"User: {st.get('user_name', '') or 'Unknown'}")
        items = st.get("reading_list", [])
        if not items:
            print("Reading List: [empty]")
        else:
            print("Reading List:")
            for i, it in enumerate(items, 1):
                print(f"  {i}. {it.get('title','(untitled)')}  [{it.get('status','queued')}]")
                if it.get("url"):   print(f"     URL: {it['url']}")
                if it.get("tags"):  print(f"     Tags: {', '.join(it['tags'])}")
                if it.get("notes"): print(f"     Notes: {it['notes']}")
        print("-" * (26 + len(label)))
    except Exception as e:
        print(f"Error displaying state: {e}")


async def process_agent_response(event):
    """Stream and log events; return final response text."""
    print(f"Event ID: {event.id}, Author: {event.author}")
    if event.content and event.content.parts:
        for part in event.content.parts:
            if getattr(part, "text", None) and part.text.strip():
                print(f"  Text: '{part.text.strip()}'")
            if getattr(part, "tool_response", None):
                print(f"  Tool Response: {part.tool_response.output}")
    if event.is_final_response():
        final_text = ""
        if event.content and event.content.parts and getattr(event.content.parts[0], "text", None):
            final_text = (event.content.parts[0].text or "").strip()
        if final_text:
            print(f"\n{Colors.BG_BLUE}{Colors.BLACK if hasattr(Colors,'BLACK') else ''}{Colors.BOLD}")
            print(f"AGENT RESPONSE:\n{final_text}")
            print(f"{Colors.RESET}")
        return final_text
    return None


async def call_agent_async(runner, user_id, session_id, query: str):
    """Send a query to the agent and return final response text."""
    content = types.Content(role="user", parts=[types.Part(text=query)])
    print(f"\n{Colors.BG_GREEN}{Colors.BOLD}--- Query: {query} ---{Colors.RESET}")
    final_response_text = None
    try:
        async for event in runner.run_async(user_id=user_id, session_id=session_id, new_message=content):
            maybe_text = await process_agent_response(event)
            if maybe_text:
                final_response_text = maybe_text
    except Exception as e:
        print(f"Error during agent call: {e}")
    return final_response_text
