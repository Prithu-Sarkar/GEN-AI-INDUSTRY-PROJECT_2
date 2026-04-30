"""
Task Definitions Module.

Rate-limit resilience applied here:
  - Task descriptions are kept intentionally concise.
    Every character in description= is an input token that counts against
    the per-minute TPM budget. The v1 descriptions were ~300 tokens each.
    These are ~140 tokens each — same analytical intent, half the cost.
  - expected_output is also short (one sentence) for the same reason.
  - output_file saves the final report automatically.
"""
import os
from crewai import Task, Agent

OUTPUT_DIR = (
    "/content/Multi-Agent Quantitative Analysis System/"
    "AAFA/crewai-agent-azure/outputs"
)


def create_tasks(quant_agent: Agent, strategist_agent: Agent, ticker: str) -> list:
    """
    Create ordered task list for the financial analysis pipeline.

    Task 1 (Quant) has no dependencies — runs first.
    Task 2 (Strategist) receives Task 1 output via context=[quant_task].

    Args:
        quant_agent: Handles numerical analysis.
        strategist_agent: Handles news and synthesis.
        ticker: Stock symbol to analyze (e.g. NVDA).

    Returns:
        list[Task]: [quant_task, recommendation_task] in execution order.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Task 1: Quantitative Analysis ──
    # Concise prompt: fetches metrics + 1yr comparison vs SPY.
    # Returns a compact structured summary (not prose).
    quant_task = Task(
        description=(
            f"Analyze {ticker} finances. "
            f"1. Use FundamentalAnalysisTool to get metrics for {ticker}. "
            f"2. Use CompareStocksTool: ticker_a={ticker}, ticker_b=SPY. "
            f"3. List any red flags (negative EPS, P/E > 50, Beta > 2). "
            f"Output: 3 bullet points max. Be concise."
        ),
        expected_output=(
            f"Bullet-point summary of {ticker} key metrics and 1yr vs SPY performance."
        ),
        agent=quant_agent,
    )

    # ── Task 2: Strategic Synthesis ──
    # Receives quant_task output via context=[quant_task].
    # Fetches 2 news articles and synthesizes final verdict.
    report_path = os.path.join(OUTPUT_DIR, f"investment_report_{ticker}.md")
    recommendation_task = Task(
        description=(
            f"Synthesize a BUY/SELL/HOLD verdict for {ticker}. "
            f"1. Read quant metrics from context. "
            f"2. Use SentimentSearchTool: query='{ticker} analyst rating news 2025'. "
            f"3. Synthesize numbers + news. Flag lawsuits or leadership changes. "
            f"4. Output a Markdown report: Executive Summary, Metrics, News, Verdict. "
            f"Be concise. No more than 400 words total."
        ),
        expected_output=(
            f"Markdown investment report for {ticker} with BUY/SELL/HOLD verdict."
        ),
        agent=strategist_agent,
        context=[quant_task],       # CrewAI injects Task 1 output here
        output_file=report_path,    # Auto-saves the Markdown report to disk
    )

    return [quant_task, recommendation_task]