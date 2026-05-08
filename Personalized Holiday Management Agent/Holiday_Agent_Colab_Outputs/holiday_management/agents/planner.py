# planner.py
# Agent 1: The Planner (Strategy Layer)
#
# Responsibilities:
#   • Parse the user request for destination, duration, and interests
#   • Generate a geographically logical day-by-day skeleton itinerary
#   • Output plain-text that the Researcher can verify fact-by-fact
#
# LLM: Groq llama-3.1-8b-instant via LangChain ≥1.2

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from holiday_management.config.settings import settings
from holiday_management.utils.state import AgentState


# ── Prompt Template ────────────────────────────────────────────────────────
PLANNER_SYSTEM_PROMPT = """You are a senior travel strategist. Your job is to create a skeleton itinerary.

Rules:
- Organise activities geographically (nearby attractions on the same day).
- Keep Day 1 light — the traveller just arrived.
- Use bullet points. Each day gets 3-4 activity placeholders.
- Do NOT invent specific prices or opening times — the Researcher will verify those.
- Output ONLY the itinerary — no preamble, no sign-off.
"""

PLANNER_HUMAN_TEMPLATE = """User request: {request}

User preferences from memory: {user_memory}

Please create a {duration_days}-day skeleton itinerary for {destination}.
"""


def build_planner_chain():
    """Construct and return the LangChain planner chain."""
    print(f"[DEBUG] Planner LLM model: {settings.LLM_MODEL}, max_tokens: {settings.LLM_MAX_TOKENS}")
    # Initialise Groq LLM — token limit kept tight to respect free-tier quotas
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=settings.GROQ_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", PLANNER_SYSTEM_PROMPT),
        ("human",  PLANNER_HUMAN_TEMPLATE),
    ])

    # Chain: prompt → LLM → plain string output
    return prompt | llm | StrOutputParser()


def run_planner(state: AgentState,
                destination: str,
                duration_days: int,
                user_memory: str = "No prior preferences recorded.") -> AgentState:
    """
    Execute the Planner agent and store the skeleton itinerary in state.

    Parameters
    ----------
    state         : Shared agent state.
    destination   : Target travel destination.
    duration_days : Number of days in the trip.
    user_memory   : Retrieved Mem0 memory snippet for personalisation.

    Returns
    -------
    AgentState : Updated state with draft_plan populated.
    """
    chain = build_planner_chain()

    draft = chain.invoke({
        "request":       state.request,
        "destination":   destination,
        "duration_days": duration_days,
        "user_memory":   user_memory,
    })

    state.draft_plan = draft
    state.add_message("planner", draft)
    return state