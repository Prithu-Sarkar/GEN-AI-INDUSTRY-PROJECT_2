"""
Reading List Curator Agent — adapted for Groq/LLaMA via LiteLLM.
Original: gemini-2.0-flash  |  Adapted: groq/llama-3.3-70b-versatile
"""
import os
from typing import List, Optional
from google.adk.agents import LlmAgent
from google.adk.tools.tool_context import ToolContext

MODEL = os.getenv("ADK_MODEL", "groq/llama-3.3-70b-versatile")

# ── Helpers ──────────────────────────────────────────────────────────

def _ensure_state(tc: ToolContext) -> None:
    """Guarantee required keys exist in state."""
    if "user_name" not in tc.state or tc.state["user_name"] is None:
        tc.state["user_name"] = ""
    if "reading_list" not in tc.state or tc.state["reading_list"] is None:
        tc.state["reading_list"] = []

def _normalize_tags(tags: Optional[List[str]]) -> List[str]:
    if not tags:
        return []
    return [str(t).strip() for t in tags if str(t).strip()]

def _valid_status(status: Optional[str]) -> bool:
    return status in {None, "queued", "reading", "done"}

# ── Tools ─────────────────────────────────────────────────────────────

def set_user_name(name: str, tool_context: ToolContext) -> dict:
    """Set the user's display name in persistent state."""
    _ensure_state(tool_context)
    old = tool_context.state.get("user_name", "")
    tool_context.state["user_name"] = name or ""
    return {
        "action": "set_user_name",
        "old_name": old,
        "new_name": tool_context.state["user_name"],
        "message": f"Saved your name as '{tool_context.state['user_name'] or 'Unknown'}'.",
    }

def add_item(
    title: str,
    url: Optional[str] = None, # Made optional with default None
    tags: Optional[List[str]] = None, # Made optional with default None
    status: Optional[str] = None, # Made optional with default None
    notes: Optional[str] = None,  # Made optional with default None
    tool_context: ToolContext = None,
) -> dict:
    """Add a new entry to the reading list.
    Fields: title (required), url (optional), tags (optional list),
    status (queued|reading|done; default queued), notes (optional).
    """
    _ensure_state(tool_context)
    if not _valid_status(status):
        status = "queued"
    item = {
        "title":  title.strip() if title else "(untitled)",
        "url":    (url or "").strip(),
        "tags":   _normalize_tags(tags),
        "status": status,
        "notes":  (notes or "").strip(),
    }
    rl = tool_context.state["reading_list"]
    rl.append(item)
    tool_context.state["reading_list"] = rl
    return {"action": "add_item", "item": item, "index": len(rl),
            "message": f"Added '{item['title']}' to your reading list."}

def list_items(
    filter_status: Optional[str] = None,
    filter_tag: Optional[str] = None,
    tool_context: ToolContext = None,
) -> dict:
    """Return the reading list, optionally filtered by status or tag."""
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]
    filtered = [
        it for it in rl
        if (not filter_status or it.get("status") == filter_status)
        and (not filter_tag or filter_tag in it.get("tags", []))
    ]
    return {"action": "list_items", "count": len(filtered), "items": filtered,
            "filters": {"status": filter_status, "tag": filter_tag},
            "message": f"Found {len(filtered)} item(s)."}

def update_item(
    index: int,
    title: Optional[str] = None,
    url: Optional[str] = None,
    status: Optional[str] = None,
    notes: Optional[str] = None,
    tags: Optional[List[str]] = None,
    tool_context: ToolContext = None,
) -> dict:
    """Update fields of an existing reading-list item (1-based index)."""
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]
    if index < 1 or index > len(rl):
        return {"action": "update_item", "status": "error",
                "message": f"No item at position {index}. You have {len(rl)} item(s)."}
    item = rl[index - 1]
    before = item.copy()
    if title  is not None: item["title"]  = title.strip() or item["title"]
    if url    is not None: item["url"]    = (url or "").strip()
    if _valid_status(status) and status is not None: item["status"] = status
    if notes  is not None: item["notes"]  = (notes or "").strip()
    if tags   is not None: item["tags"]   = _normalize_tags(tags)
    rl[index - 1] = item
    tool_context.state["reading_list"] = rl
    return {"action": "update_item", "index": index, "before": before,
            "after": item, "message": f"Updated item {index} ('{before.get('title', '')}')."}

def annotate_item(index: int, notes: str, tool_context: ToolContext) -> dict:
    """Append or set notes for an item (1-based index)."""
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]
    if index < 1 or index > len(rl):
        return {"action": "annotate_item", "status": "error",
                "message": f"No item at position {index}. You have {len(rl)} item(s)."}
    item = rl[index - 1]
    before_notes = item.get("notes", "")
    item["notes"] = (notes or "").strip()
    rl[index - 1] = item
    tool_context.state["reading_list"] = rl
    return {"action": "annotate_item", "index": index, "old_notes": before_notes,
            "new_notes": item["notes"], "message": f"Noted item {index} ('{item.get('title', '')}')."}

def remove_item(index: int, tool_context: ToolContext) -> dict:
    """Remove a reading-list item (1-based index)."""
    _ensure_state(tool_context)
    rl = tool_context.state["reading_list"]
    if index < 1 or index > len(rl):
        return {"action": "remove_item", "status": "error",
                "message": f"No item at position {index}. You have {len(rl)} item(s)."}
    removed = rl.pop(index - 1)
    tool_context.state["reading_list"] = rl
    return {"action": "remove_item", "index": index, "removed": removed,
            "message": f"Removed '{removed.get('title', '')}' from your reading list."}

# ── Agent ─────────────────────────────────────────────────────────────

reading_agent = LlmAgent(
    name="reading_list_curator",
    model=MODEL,
    description="Curate a personal reading list with persistent memory.",
    instruction="""
You are a friendly Reading List Curator. The session state contains:
  - user_name: the user's display name (string, may be empty)
  - reading_list: an array of items, each with {title, url, tags[], status, notes}

Your job:
  1) Greet the user by name if known.
  2) Understand natural-language requests and call the appropriate tools.
  3) Return a short, helpful summary after tool calls.

Tool selection:
  - "add" requests   → add_item  (title required; url/tags/status/notes optional; default status=queued)
  - "show/list"      → list_items (pass filter_status or filter_tag if mentioned)
  - update fields    → update_item (infer 1-based index from phrasing)
  - add/replace notes→ annotate_item
  - delete/remove    → remove_item
  - user shares name → set_user_name

Formatting: numbered list — Title [status], then url/tags/notes on sub-lines if present.
Be concise. Never fabricate URLs or tags.
    """,
    tools=[set_user_name, add_item, list_items, update_item, annotate_item, remove_item],
)

root_agent = reading_agent  # ADK auto-discovery alias
