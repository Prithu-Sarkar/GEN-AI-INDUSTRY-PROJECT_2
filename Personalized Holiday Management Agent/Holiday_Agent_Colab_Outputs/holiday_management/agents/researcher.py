# researcher.py
# Agent 2: The Researcher (Data Verification Layer)
#
# Responsibilities:
#   • Take the Planner's skeleton itinerary
#   • For each activity, simulate fact-checking (addresses, hours, tips)
#   • Return an enriched final itinerary in Markdown
#
# In production: swap the simulated facts with real API calls
# (Google Places API, TripAdvisor, Booking.com, etc.)

import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from holiday_management.config.settings import settings
from holiday_management.utils.state import AgentState


# ── Prompt Template ────────────────────────────────────────────────────────
RESEARCHER_SYSTEM_PROMPT = """You are a meticulous travel fact-checker and content writer.

You receive a skeleton itinerary and must produce the FINAL, enriched travel guide.

Rules:
- For each activity, add realistic (but clearly labelled as approximate) details:
    * Best time to visit
    * Practical tip (e.g. book in advance, wear comfortable shoes)
    * Approximate cost bracket (budget / moderate / splurge)
- Use clean Markdown formatting with Day headers (## Day 1, ## Day 2, ...).
- End with a "## Practical Tips" section covering transport, language, currency.
- NEVER fabricate specific URLs or phone numbers.
- Be concise — max 80 words per day.
"""

RESEARCHER_HUMAN_TEMPLATE = """Destination: {destination}
Duration: {duration_days} days

Skeleton Itinerary (from Planner):
{draft_plan}

Please produce the enriched, final travel guide.
"""


def build_researcher_chain():
    """Construct and return the LangChain researcher chain."""
    print(f"[DEBUG] Researcher LLM model: {settings.LLM_MODEL}, max_tokens: {settings.LLM_MAX_TOKENS}")
    llm = ChatGroq(
        model=settings.LLM_MODEL,
        temperature=0.2,                  # lower temp for factual enrichment
        max_tokens=settings.LLM_MAX_TOKENS,
        api_key=settings.GROQ_API_KEY
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", RESEARCHER_SYSTEM_PROMPT),
        ("human",  RESEARCHER_HUMAN_TEMPLATE),
    ])

    return prompt | llm | StrOutputParser()


def run_researcher(state: AgentState,
                   destination: str,
                   duration_days: int) -> AgentState:
    """
    Execute the Researcher agent on the Planner's draft plan.

    Parameters
    ----------
    state         : Shared agent state (must have draft_plan populated).
    destination   : Target travel destination.
    duration_days : Number of trip days.

    Returns
    -------
    AgentState : Updated state with final_output populated.
    """
    if not state.draft_plan:
        raise ValueError("Researcher requires a draft_plan — run Planner first.")

    chain = build_researcher_chain()

    final = chain.invoke({
        "destination":   destination,
        "duration_days": duration_days,
        "draft_plan":    state.draft_plan,
    })

    state.final_output = final
    state.add_message("researcher", final)
    return state