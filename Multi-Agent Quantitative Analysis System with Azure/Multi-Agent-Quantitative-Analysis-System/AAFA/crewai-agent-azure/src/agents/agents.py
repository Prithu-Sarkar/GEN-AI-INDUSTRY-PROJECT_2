"""
Agent Definitions Module.

Defines the two AI personas in the financial analysis crew:

  1. Quantitative Analyst  -- hard numbers (P/E, Beta, EPS), uses Yahoo Finance tools.
  2. Investment Strategist -- qualitative news + final recommendation, uses Firecrawl.

Both agents use Groq LLaMA Instant via the LiteLLM integration layer.
"""

import os
from typing import Tuple
from crewai import Agent, LLM
from src.agents.tools.financial import FundamentalAnalysisTool, CompareStocksTool
from src.agents.tools.scraper import SentimentSearchTool
from src.shared.config import settings


def _build_llm() -> LLM:
    """
    Constructs the CrewAI LLM object pointing to Groq LLaMA Instant.

    Uses LiteLLM under the hood; model string format: "groq/<model_name>".
    Sets GROQ_API_KEY in environment so LiteLLM can authenticate.

    Returns:
        LLM: A configured CrewAI LLM instance.
    """
    # Ensure the API key is visible to LiteLLM via environment
    os.environ["GROQ_API_KEY"] = settings.groq_api_key

    return LLM(
        model=settings.groq_model,           # e.g. "groq/llama-3.1-8b-instant"
        api_key=settings.groq_api_key,
        temperature=0.1,                     # Low temperature for deterministic financial analysis
        max_tokens=1024,                     # Sufficient for detailed investment reports
    )


def create_agents() -> Tuple[Agent, Agent]:
    """
    Factory function that instantiates both agents for the financial crew.

    Returns:
        Tuple[Agent, Agent]: (quant_agent, strategist_agent)
    """
    # Shared LLM instance — both agents use the same Groq backend
    llm = _build_llm()

    # ── Agent 1: Quantitative Analyst ────────────────────────────────────────
    # Persona: a veteran Wall Street quant who trusts only hard numbers.
    # Tools: FundamentalAnalysisTool (snapshot) + CompareStocksTool (1-year return).
    # allow_delegation=False: this agent never passes work to others.
    quant_agent = Agent(
        role="Senior Quantitative Analyst",
        goal="Analyze the financial health and historical performance of the target stock.",
        backstory=(
            "You are a veteran financial analyst with 20 years of experience on Wall Street. "
            "You do not care about rumors or news headlines. You only trust hard data. "
            "You judge companies strictly by their balance sheets, P/E ratios, "
            "earnings growth (EPS), and volatility (Beta). "
            "Your reports are concise, number-heavy, and brutally honest."
        ),
        llm=llm,
        tools=[
            FundamentalAnalysisTool(),
            CompareStocksTool(),
        ],
        verbose=True,
        memory=False,           # Disabled: memory requires external embedding service
        allow_delegation=False,
    )

    # ── Agent 2: Investment Strategist ────────────────────────────────────────
    # Persona: a visionary strategist who reads news and makes the final call.
    # Tools: SentimentSearchTool (Firecrawl news scraper).
    # context=[quant_task]: receives the Quant output before reasoning.
    strategist_agent = Agent(
        role="Chief Investment Strategist",
        goal="Synthesize quantitative data with market sentiment to form a final recommendation.",
        backstory=(
            "You are a visionary investment strategist who looks beyond the spreadsheet. "
            "You understand that stock prices are driven by human psychology, news, "
            "and leadership changes. You read the news to find the narrative "
            "behind the stock. You combine the Quant numbers with your news findings "
            "to give a final Buy, Sell, or Hold recommendation."
        ),
        llm=llm,
        tools=[
            SentimentSearchTool(),
        ],
        verbose=True,
        memory=False,
        allow_delegation=False,
    )

    return quant_agent, strategist_agent