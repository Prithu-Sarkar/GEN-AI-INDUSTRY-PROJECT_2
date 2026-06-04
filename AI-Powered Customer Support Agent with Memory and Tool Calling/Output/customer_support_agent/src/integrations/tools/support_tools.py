
from __future__ import annotations
import hashlib, json, os, sqlite3, sys

# LangChain 1.2+ canonical import for @tool decorator
from langchain_core.tools import tool

sys.path.insert(0,"/content/customer_support_agent/src")
from core.settings import get_settings

def _bucket(email,size): return int(hashlib.sha256(email.strip().lower().encode()).hexdigest(),16)%size
def _j(d): return json.dumps(d)
def _band(n): return "light" if n<=1 else ("moderate" if n<=3 else "heavy")

@tool
def lookup_customer_plan(customer_email: str)->str:
    """Return subscription plan and SLA for a customer email.
    Args: customer_email: customer email string.
    Returns: JSON with tool, customer_email, summary, details, recommended_action."""
    plans=[{"plan_tier":"free","sla_hours":48,"priority_queue":False},
           {"plan_tier":"starter","sla_hours":24,"priority_queue":False},
           {"plan_tier":"pro","sla_hours":8,"priority_queue":True},
           {"plan_tier":"enterprise","sla_hours":1,"priority_queue":True}]
    p=plans[_bucket(customer_email,len(plans))]
    return _j({"tool":"lookup_customer_plan","customer_email":customer_email,
               "summary":f"{customer_email} on {p['plan_tier']} plan, SLA {p['sla_hours']}h.",
               "details":p,"recommended_action":"Priority." if p["priority_queue"] else "Standard."})

@tool
def lookup_open_ticket_load(customer_email: str)->str:
    """Return open ticket count for a customer from SQLite.
    Args: customer_email: customer email string.
    Returns: JSON with tool, customer_email, summary, details, recommended_action."""
    s=get_settings()
    conn=sqlite3.connect(str(s.db_path)); conn.row_factory=sqlite3.Row
    row=conn.execute("SELECT id FROM customers WHERE email=?",(customer_email.strip().lower(),)).fetchone()
    if not row:
        conn.close()
        return _j({"tool":"lookup_open_ticket_load","customer_email":customer_email,
                   "summary":f"No record for {customer_email}.",
                   "details":{"customer_found":False,"open_tickets":None,"load_band":"unknown"},
                   "recommended_action":"Verify email."})
    cnt=conn.execute("SELECT COUNT(*) AS c FROM tickets t JOIN customers cu ON cu.id=t.customer_id "
                     "WHERE cu.email=? AND t.status='open'",(customer_email.strip().lower(),)).fetchone()["c"]
    conn.close(); n=int(cnt)
    return _j({"tool":"lookup_open_ticket_load","customer_email":customer_email,
               "summary":f"{customer_email} has {n} open ticket(s). Load: {_band(n)}.",
               "details":{"customer_found":True,"open_tickets":n,"load_band":_band(n)},
               "recommended_action":"Acknowledge multiple issues." if n>1 else "Isolated incident."})

def get_support_tools(include_web_search=True)->list:
    """Return all LangChain tools for the agent."""
    tools=[lookup_customer_plan,lookup_open_ticket_load]
    if include_web_search and os.getenv("TAVILY_API_KEY"):
        try:
            # LangChain 1.2+ community import for Tavily
            from langchain_community.tools.tavily_search import TavilySearchResults
            tools.append(TavilySearchResults(max_results=3))
            print("  Tavily web-search tool added.")
        except Exception as e: print(f"  Tavily skipped: {e}")
    return tools
