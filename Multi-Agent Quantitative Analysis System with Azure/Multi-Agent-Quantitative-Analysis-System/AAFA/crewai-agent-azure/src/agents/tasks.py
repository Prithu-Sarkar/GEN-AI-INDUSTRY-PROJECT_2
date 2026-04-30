"""
Task Definitions Module.

Defines the specific work orders (Tasks) given to each agent.
This is the prompt-engineering layer: precise descriptions drive quality output.

Key design:
  - Task 1 (Quant): collects hard numbers via tool calls.
  - Task 2 (Strategist): receives Task 1 output as context, then adds news + verdict.
  - output_file: CrewAI automatically writes the final report to disk.
"""

import os
from crewai import Task, Agent

# Directory where CrewAI will write the final report file
OUTPUT_DIR = (
    '/content/Multi-Agent Quantitative Analysis System/AAFA/crewai-agent-azure/outputs'
)


def create_tasks(quant_agent: Agent, strategist_agent: Agent, ticker: str) -> list:
    """
    Creates the ordered list of tasks for the financial analysis pipeline.

    Args:
        quant_agent (Agent): Handles numerical analysis tasks.
        strategist_agent (Agent): Handles qualitative synthesis tasks.
        ticker (str): Stock symbol to analyze (e.g. 'NVDA').

    Returns:
        list[Task]: [quant_task, recommendation_task] in execution order.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # ── Task 1: Quantitative Data Collection ─────────────────────────────────
    # The Quant agent fetches raw numbers and computes relative performance.
    # This task has no context dependency — it runs first.
    quant_task = Task(
        description=(
            f"Analyze the financial health of ticker {ticker}. "
            f"Step 1: Use FundamentalAnalysisTool to fetch P/E, EPS, Beta, and Market Cap for {ticker}. "
            f"Step 2: Use CompareStocksTool to compare {ticker} against SPY to see its relative 1-year performance. "
            f"Step 3: Identify any major numerical red flags such as negative EPS or extremely high P/E. "
            f"Output a concise summary of the hard numbers with clear section headers."
        ),
        expected_output=(
            "A structured summary of financial metrics and 1-year performance comparison "
            "formatted with clear sections for Metrics and Performance."
        ),
        agent=quant_agent,
    )

    # ── Task 2: Strategic Synthesis and Recommendation ────────────────────────
    # The Strategist agent reads Task 1 output, searches for news,
    # and synthesises a final BUY / SELL / HOLD verdict in Markdown.
    # context=[quant_task] is the CrewAI mechanism for passing prior output.
    report_path = os.path.join(OUTPUT_DIR, f"investment_report_{ticker}.md")
    recommendation_task = Task(
        description=(
            f"Formulate a final investment recommendation for {ticker}. "
            f"Step 1: Read the financial metrics provided by the Quantitative Analyst from context. "
            f"Step 2: Use SentimentSearchTool to find the top 3 recent news articles or analyst ratings for {ticker}. "
            f"  Look for leadership changes, regulatory lawsuits, or product launches. "
            f"Step 3: Synthesize the numbers from the Quant with the narrative from the News. "
            f"  If numbers are good but news is bad such as a lawsuit, be cautious. "
            f"  If numbers are bad but news is hype, be skeptical. "
            f"Step 4: Provide a final verdict of BUY, SELL, or HOLD with clear reasoning. "
            f"Format the output as a professional Markdown investment report."
        ),
        expected_output=(
            "A comprehensive Markdown investment report including: "
            "Executive Summary, Key Metrics, News Analysis, Risk Factors, and Final Verdict."
        ),
        agent=strategist_agent,
        context=[quant_task],           # Inject Quant output as context for the Strategist
        output_file=report_path,        # CrewAI writes the final report here automatically
    )

    return [quant_task, recommendation_task]