"""
Minimal HTTP client for the ADK API Server (unchanged from course).
Used by Streamlit app and curl-equivalent scripts.
"""
import os, time, requests
from typing import Any, Dict, Optional

API_BASE = os.getenv("ADK_API_BASE", "http://localhost:8000")


class ADKClient:
    """Thin wrapper: create session + run one turn."""

    def __init__(self, api_base: Optional[str] = None):
        self.api_base = api_base or API_BASE

    def create_session(self, app_name: str, user_id: str,
                       session_id: Optional[str] = None) -> str:
        sid = session_id or f"session-{int(time.time())}"
        url = f"{self.api_base}/apps/{app_name}/users/{user_id}/sessions/{sid}"
        requests.post(url, headers={"Content-Type": "application/json"},
                      json={}).raise_for_status()
        return sid

    def run(self, app_name: str, user_id: str, session_id: str,
            message: str) -> Dict[str, Any]:
        payload = {
            "app_name": app_name, "user_id": user_id, "session_id": session_id,
            "new_message": {"role": "user", "parts": [{"text": message}]},
        }
        r = requests.post(f"{self.api_base}/run",
                          headers={"Content-Type": "application/json"},
                          json=payload)
        r.raise_for_status()
        try:    return r.json()
        except: return {"raw": r.text}

    @staticmethod
    def parse_events_for_text(resp: Dict[str, Any]) -> str:
        """Extract final assistant text from ADK event payload."""
        events = resp if isinstance(resp, list) else resp.get("events", [resp])
        final_text = ""
        for ev in events:
            content = ev.get("content", {})
            parts = content.get("parts", []) if isinstance(content, dict) else []
            for p in parts:
                if isinstance(p.get("text"), str) and p["text"].strip():
                    final_text = p["text"].strip()
        return final_text
