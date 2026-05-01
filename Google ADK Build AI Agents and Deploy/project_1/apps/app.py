"""
ADK API + Streamlit — Simple Q&A app (unchanged from course).
Run locally after launching: adk api_server -v project_1/
    streamlit run project_1/apps/app.py
"""
from __future__ import annotations
import os, uuid, json, requests
import streamlit as st

API_DEFAULT  = os.getenv("ADK_API_BASE", "http://localhost:8000")
APP_DEFAULT  = os.getenv("ADK_APP_SIMPLE", "simple")
USER_DEFAULT = os.getenv("ADK_USER_ID", f"user-{uuid.uuid4()}")

st.set_page_config(page_title="ADK + Streamlit: Simple Q&A", layout="centered")
st.title("Q&A — ADK API + Streamlit")
st.caption("Frontend: Streamlit  ·  Backend: ADK API  ·  Model: Groq/LLaMA")

for k, v in [("api_base", API_DEFAULT), ("app_name", APP_DEFAULT),
              ("user_id", USER_DEFAULT), ("session_id", None), ("events", [])]:
    if k not in st.session_state:
        st.session_state[k] = v

def GET(url):
    r = requests.get(url, timeout=60); r.raise_for_status(); return r.json()

def POST(url, payload):
    r = requests.post(url, json=payload,
                      headers={"Content-Type": "application/json"}, timeout=120)
    r.raise_for_status()
    try:    return r.json()
    except: return {"raw": r.text}

def create_session():
    sid = f"session-{uuid.uuid4()}"
    url = (f"{st.session_state.api_base}/apps/{st.session_state.app_name}"
           f"/users/{st.session_state.user_id}/sessions/{sid}")
    requests.post(url, json={}, headers={"Content-Type": "application/json"},
                  timeout=60).raise_for_status()
    st.session_state.session_id = sid
    return sid

def run_turn(question):
    return POST(f"{st.session_state.api_base}/run", {
        "app_name":   st.session_state.app_name,
        "user_id":    st.session_state.user_id,
        "session_id": st.session_state.session_id,
        "new_message": {"role": "user", "parts": [{"text": question}]},
    })

def normalize_events(resp):
    if isinstance(resp, list): return resp
    if isinstance(resp, dict) and isinstance(resp.get("events"), list):
        return resp["events"]
    return []

def last_text(events):
    text = ""
    for ev in events:
        for p in (ev.get("content") or {}).get("parts", []):
            if isinstance(p.get("text"), str) and p["text"].strip():
                text = p["text"].strip()
    return text

# ── Sidebar
with st.sidebar:
    st.subheader("Server & Session")
    st.text_input("ADK API Base", key="api_base")
    st.text_input("App Name",     key="app_name")
    st.text_input("User ID",      key="user_id")
    if st.button("Create / Reset Session", use_container_width=True):
        try:    st.success(f"Session: {create_session()}")
        except requests.HTTPError as e: st.error(str(e))
    if st.session_state.session_id:
        st.info(f"Active: {st.session_state.session_id}")
    else:
        st.warning("Create a session to begin.")

# ── Main
st.divider()
q   = st.text_input("Your question", "What is retrieval augmented generation?")
ask = st.button("Ask")
show_raw = st.checkbox("Show raw events", value=False)

if st.session_state.session_id and ask:
    try:
        resp   = run_turn(q)
        events = normalize_events(resp)
        st.session_state.events = events
        st.success("Answer:")
        st.write(last_text(events) or "_(No final text found)_")
    except requests.HTTPError as e:
        st.error(f"/run failed: {e}")

if show_raw and st.session_state.events:
    st.subheader("Raw events")
    st.code(json.dumps(st.session_state.events, indent=2), language="json")
