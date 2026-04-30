"""
Agent Definitions Module.

Rate-limit resilience applied here:
  - LLM max_tokens=1024: Each response is capped. Without this, a verbose
    agent can generate 3000+ token responses and exhaust the TPM budget in
    a single call. 1024 tokens is sufficient for structured analysis steps.
  - Inter-step delay via step_callback: A 5-second pause after each LLM
    call spreads token consumption across time, keeping TPM under the limit.
  - memory=False: CrewAI memory requires an embedding model API call which
    adds hidden token usage. Disabled for free-tier compatibility.
"""
import os
import time
from typing import Tuple
from crewai import Agent, LLM
from src.agents.tools.financial import FundamentalAnalysisTool, CompareStocksTool
from src.agents.tools.scraper import SentimentSearchTool
from src.shared.config import settings


def _inter_step_delay(step_output) -> None:
    """
    step_callback injected into each agent.

    Adds a 5-second pause after every LLM reasoning step.
    This is the most reliable mechanism for staying under TPM limits:
    if each step consumes ~1000 tokens and we wait 5 seconds between steps,
    the effective rate is 12,000 tokens/minute — comfortably within 6,000
    because actual LLM calls are spaced by tool execution time too.

    Args:
        step_output: CrewAI step output object (contents not used here).
    """
    print("  [Rate-limit guard] Pausing 5s between steps...")
    time.sleep(5)


def _build_llm() -> LLM:
    """
    Build the Groq LLM object with rate-limit-safe parameters.

    max_tokens=1024: The single most effective rate-limit fix.
    Without this cap, CrewAI's default allows responses up to the model
    context limit (~32K), which can exhaust 6000 TPM in a single call.

    Returns:
        LLM: Configured CrewAI LLM instance.
    """
    os.environ["GROQ_API_KEY"] = settings.groq_api_key
    return LLM(
        model=settings.groq_model,        # groq/llama-3.3-70b-versatile
        api_key=settings.groq_api_key,
        temperature=settings.temperature, # 0.1 for deterministic output
        max_tokens=settings.max_tokens,   # 1024 — hard cap per response
    )


def create_agents() -> Tuple[Agent, Agent]:
    """
    Instantiate both AI agents with rate-limit-resilient configuration.

    Returns:
        Tuple[Agent, Agent]: (quant_agent, strategist_agent)
    """
    llm = _build_llm()

    # ── Agent 1: Quantitative Analyst ──
    # Backstory trimmed vs v1 (~50% shorter) to reduce system prompt tokens.
    # Same analytical persona is conveyed with fewer words.
    quant_agent = Agent(
        role="Senior Quantitative Analyst",
        goal="Analyze the financial health and 1-year performance of the target stock.",
        backstory=(
            "A veteran Wall Street quant with 20 years experience. "
            "Trusts only hard data: P/E ratios, EPS, Beta, and relative performance. "
            "Produces concise, number-focused summaries with no fluff."
        ),
        llm=llm,
        tools=[FundamentalAnalysisTool(), CompareStocksTool()],
        verbose=True,
        memory=False,            # Disabled: embedding calls consume hidden TPM
        allow_delegation=False,
        step_callback=_inter_step_delay,  # 5s pause between LLM calls
    )

    # ── Agent 2: Investment Strategist ──
    strategist_agent = Agent(
        role="Chief Investment Strategist",
        goal="Synthesize quant data with news sentiment. Deliver BUY/SELL/HOLD verdict.",
        backstory=(
            "A visionary strategist who reads market narratives. "
            "Combines quant numbers with live news to form clear investment verdicts. "
            "Skeptical of hype; cautious about regulatory and macro risks."
        ),
        llm=llm,
        tools=[SentimentSearchTool()],
        verbose=True,
        memory=False,
        allow_delegation=False,
        step_callback=_inter_step_delay,
    )

    return quant_agent, strategist_agent