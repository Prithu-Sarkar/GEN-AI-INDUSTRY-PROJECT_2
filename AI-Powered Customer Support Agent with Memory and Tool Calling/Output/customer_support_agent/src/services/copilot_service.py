
from __future__ import annotations
import json, re
from typing import Any

# ── LangChain 1.2+ imports ─────────────────────────────────────────────────
from langchain_core.messages import (
    AIMessage, BaseMessage, HumanMessage, SystemMessage, ToolMessage
)
from langchain_groq import ChatGroq

# ── LangGraph 0.2+ imports ─────────────────────────────────────────────────
from langgraph.prebuilt          import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from core.settings import Settings
from integrations.memory.faiss_memory import CustomerMemoryStore
from integrations.rag.faiss_kb        import KnowledgeBaseService
from integrations.tools.support_tools import get_support_tools


class SupportCopilot:
    """LangGraph ReAct agent with FAISS memory + RAG."""

    def __init__(self, settings: Settings):
        if not settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY missing. Add in Colab -> Tools -> Secrets.")
        self._s=settings
        # Instant model for agent tool-calling loop (fast, cheap)
        self._llm_instant=ChatGroq(
            model=settings.groq_model_instant, groq_api_key=settings.groq_api_key,
            temperature=settings.llm_temperature, max_tokens=settings.max_tokens_per_call)
        # Versatile model for fallback synthesis (smarter)
        self._llm_versatile=ChatGroq(
            model=settings.groq_model_versatile, groq_api_key=settings.groq_api_key,
            temperature=settings.llm_temperature, max_tokens=settings.max_tokens_per_call)
        # LangGraph 0.2+ ReAct agent + MemorySaver checkpoint
        self._tools=get_support_tools(include_web_search=True)
        self._agent=create_react_agent(
            model=self._llm_instant,
            tools=self._tools,
            checkpointer=MemorySaver())
        self.rag=KnowledgeBaseService(settings=settings)
        self._mem_error=None
        try: self.memory=CustomerMemoryStore(settings=settings)
        except Exception as e: self._mem_error=str(e); self.memory=None

    # ── Public API ──────────────────────────────────────────────────────────

    def generate_draft(self,ticket:dict,customer:dict)->dict:
        """Generate draft reply. Returns {draft, context_used}."""
        query=f"{ticket['subject']}\n{ticket['description']}"
        mem_hits=self._fetch_memories(query,customer["email"],customer.get("company"))
        kb_hits=self.rag.search(query=query,top_k=self._s.rag_top_k)
        sys_msg=SystemMessage(content=self._system_prompt(mem_hits,kb_hits))
        usr_msg=HumanMessage(content=self._user_prompt(ticket,customer))
        result=self._agent.invoke(
            {"messages":[sys_msg,usr_msg]},
            config={"configurable":{"thread_id":self._thread_id(ticket,customer)},
                    "recursion_limit":20})
        draft,tool_calls=self._parse(result)
        used_fb=False
        if not draft:
            draft=self._llm_fallback(ticket,customer,mem_hits,kb_hits,tool_calls)
            used_fb=True
        if not draft:
            draft=self._det_fallback(ticket,customer,tool_calls)
            used_fb=True
        ctx=self._build_ctx(ticket,customer,mem_hits,kb_hits,tool_calls)
        if self._mem_error: ctx.setdefault("errors",[]).append(f"Memory disabled: {self._mem_error}")
        if used_fb: ctx.setdefault("errors",[]).append("Fallback synthesis used.")
        ctx["agent_runtime"]="langgraph_create_react_agent_v0.2"
        return {"draft":draft,"context_used":ctx}

    def save_accepted_resolution(self,customer_email,customer_company,ticket_subject,
                                  ticket_description,draft_content,context_used=None):
        """Persist accepted draft to FAISS memory for future context."""
        if self.memory is None: return
        ents=self._ent_links(ticket_subject,ticket_description,draft_content,context_used or {})
        for uid in self._scope_ids(customer_email,customer_company):
            self.memory.add_resolution(uid,ticket_subject,ticket_description,draft_content,ents)

    def search_customer_memories(self,customer_email,query,customer_company=None,limit=10):
        return self._fetch_memories(query,customer_email,customer_company,limit)

    # ── Private helpers ──────────────────────────────────────────────────────

    def _fetch_memories(self,query,email,company,limit=None):
        if self.memory is None: return []
        lim=limit or self._s.mem_top_k; hits=[]
        for uid in self._scope_ids(email,company):
            hits.extend(self.memory.search(query=query,user_id=uid,limit=lim))
        return self._dedupe(hits,lim)

    @staticmethod
    def _scope_ids(email,company):
        ids=[email.strip().lower()]
        if company:
            n=re.sub(r"[^a-z0-9]+","-",company.strip().lower()).strip("-")
            if n: ids.append(f"company::{n}")
        return ids

    @staticmethod
    def _dedupe(hits,limit):
        seen,out=set(),[]
        for h in hits:
            k=str(h.get("memory","")).strip().lower()
            if not k or k in seen: continue
            seen.add(k); out.append(h)
            if len(out)>=limit: break
        return out

    def _system_prompt(self,mem_hits,kb_hits)->str:
        """Build system prompt with memory + KB context injection."""
        mem_block=("\n".join(f"- {h['memory'][:160]}" for h in mem_hits)
                   if mem_hits else "- No prior memories found.")
        kb_block=("\n".join(f"- [{h['source']}] {h['content'][:180]}" for h in kb_hits)
                  if kb_hits else "- No KB chunks found.")
        return (
            "You are an AI copilot for customer support agents. "
            "Write concise, empathetic, actionable draft replies.\n"
            "Call tools when ticket implies billing, plan, or account checks.\n\n"
            f"=== Customer Memory ===\n{mem_block}\n\n"
            f"=== Knowledge Base ===\n{kb_block}\n\n"
            "Rules:\n"
            "1. Open with empathy and direct acknowledgement.\n"
            "2. Provide clear next steps.\n"
            "3. Reference KB/tool data; never expose internal reasoning.\n"
            "4. Keep reply under 150 words."
        )

    @staticmethod
    def _user_prompt(ticket,customer)->str:
        return (f"Customer: {customer.get('name') or 'Unknown'} ({customer['email']})"
                f"\nCompany: {customer.get('company') or 'Unknown'}"
                f"\nSubject: {ticket['subject']}  Priority: {ticket.get('priority','medium')}"
                f"\nDescription:\n{ticket['description'][:500]}"
                "\n\nWrite draft. Call tools if billing/plan check needed.")

    @staticmethod
    def _thread_id(ticket,customer):
        tid=ticket.get("id")
        return f"ticket::{tid}" if tid else f"ticket::{customer.get('email','?')}"  

    def _parse(self,result):
        """Extract final draft text + tool call trace from LangGraph result."""
        raw=(result.get("messages",[]) if isinstance(result,dict)
             else getattr(result,"messages",[]))
        msgs=[m for m in raw if isinstance(m,BaseMessage)]
        draft=""
        for m in reversed(msgs):
            if isinstance(m,AIMessage):
                c=self._cstr(m).strip()
                if c: draft=c; break
        tm_by_id={m.tool_call_id:m for m in msgs
                  if isinstance(m,ToolMessage) and m.tool_call_id}
        tool_calls=[]
        for m in msgs:
            if not isinstance(m,AIMessage): continue
            for call in (getattr(m,"tool_calls",None) or []):
                name=call.get("name","?"); cid=call.get("id")
                tr={"tool_name":name,"tool_call_id":cid,"arguments":call.get("args",{})}
                tm=tm_by_id.get(str(cid)) if cid else None
                if tm is None:
                    tr.update({"status":"skipped","summary":f"{name} had no result.",
                               "output":None,"output_text":""})
                else:
                    raw_out=self._cstr(tm)
                    parsed=self._parse_json(raw_out)
                    tr.update({"status":"error" if getattr(tm,"status",None)=="error" else "ok",
                               "summary":(parsed or {}).get("summary") or raw_out[:120],
                               "output":parsed,"output_text":raw_out})
                tool_calls.append(tr)
        return draft,tool_calls

    @staticmethod
    def _cstr(m):
        c=getattr(m,"content",m)
        return "\n".join(str(x) for x in c) if isinstance(c,list) else str(c)

    @staticmethod
    def _parse_json(raw):
        try:
            p=json.loads(raw)
            return p if isinstance(p,dict) else None
        except: return None

    def _llm_fallback(self,ticket,customer,mem_hits,kb_hits,tool_calls)->str:
        """Fallback: ask versatile model directly without tool loop."""
        prompt=(f"Customer: {customer.get('name')} ({customer.get('email')})"
                f"\nSubject: {ticket.get('subject')}\nDesc: {ticket.get('description','')[:400]}"
                f"\nMemory: {[h['memory'][:120] for h in mem_hits[:2]] or ['none']}"
                f"\nKB: {[h['content'][:120] for h in kb_hits[:2]] or ['none']}"
                f"\nTools: {[str(t.get('summary',''))[:120] for t in tool_calls] or ['none']}"
                "\n\nWrite concise empathetic draft reply under 150 words.")
        try:
            resp=self._llm_versatile.invoke([
                SystemMessage(content="You are an AI support copilot. Produce ONLY the final reply."),
                HumanMessage(content=prompt)])
            return self._cstr(resp).strip()
        except: return ""

    @staticmethod
    def _det_fallback(ticket,customer,tool_calls)->str:
        """Last-resort deterministic template — guaranteed non-empty."""
        name=customer.get("name") or customer.get("email") or "there"
        best=next((str(t.get("summary","")).strip() for t in tool_calls if t.get("summary")),
                  "Our support team is reviewing your issue.")
        return (f"Hi {name},\n\nThank you for contacting us about '" +
                ticket.get("subject","your issue") +
                f"'.'\n\n{best}\n\nBest regards,\nSupport Team")

    def _build_ctx(self,ticket,customer,mem_hits,kb_hits,tool_calls)->dict:
        """Build structured context_used dict (v2 schema) for auditability."""
        return {
            "version":2,
            "ticket":{"id":ticket.get("id"),"subject":ticket.get("subject"),
                      "priority":ticket.get("priority"),"status":ticket.get("status")},
            "customer":{"id":customer.get("id"),"email":customer.get("email"),
                        "name":customer.get("name"),"company":customer.get("company")},
            "signals":{"memory_hit_count":len(mem_hits),"knowledge_hit_count":len(kb_hits),
                       "tool_call_count":len(tool_calls),
                       "knowledge_sources":list({h.get("source") for h in kb_hits})},
            "highlights":{"memory":[str(h.get("memory",""))[:160] for h in mem_hits[:3]],
                           "knowledge":[f"[{h.get('source')}] {h.get('content','')[:160]}" for h in kb_hits[:3]],
                           "tools":[str(t.get("summary",""))[:160] for t in tool_calls[:3]]},
            "memory_hits":mem_hits,"knowledge_hits":kb_hits,"tool_calls":tool_calls}

    def _ent_links(self,subject,description,draft,context)->list:
        """Extract entity tags for memory annotation."""
        merged=f"{subject}\n{description}\n{draft}".lower()
        links=[]
        for code in re.findall(r"\b([45]\d\d)\b",merged)[:4]: links.append(f"http:{code}")
        for region,markers in [("India",["india"," in "]),("EU",["europe"]),("US",["united states"])]:
            if any(m in merged for m in markers): links.append(f"region:{region}")
        for tc in context.get("tool_calls",[]):
            d=(tc.get("output") or {}).get("details") or {}
            if isinstance(d,dict) and d.get("plan_tier"): links.append(f"plan:{d['plan_tier']}")
        return list(dict.fromkeys(links))[:12]
