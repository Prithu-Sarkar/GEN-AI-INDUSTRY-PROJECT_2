"""
Crew Orchestration Module.

Assembles the AI team (Crew), assigns tasks, and manages sequential execution.
This is the entry point for the agentic pipeline.

Execution order is enforced by Process.sequential:
  Quant Agent completes fully -> Strategist Agent receives output -> writes report.
"""

from crewai import Crew, Process
from src.agents.agents import create_agents
from src.agents.tasks import create_tasks


def run_financial_crew(ticker: str) -> str:
    """
    Initializes and executes the Financial Analysis Crew for a given stock.

    Workflow:
        1. Instantiate both agents (Quant + Strategist) with Groq LLaMA.
        2. Create ordered task list with context chaining.
        3. Assemble Crew with sequential execution process.
        4. Kick off the analysis and return the string result.

    Args:
        ticker (str): Stock symbol to analyze (e.g. 'MSFT').

    Returns:
        str: The final Markdown investment report as a string.
    """
    # Step 1: Instantiate the agent personas
    quant_agent, strategist_agent = create_agents()

    # Step 2: Create dynamic tasks for the given ticker
    # Each task description is rendered with the actual ticker symbol
    tasks = create_tasks(
        quant_agent=quant_agent,
        strategist_agent=strategist_agent,
        ticker=ticker,
    )

    # Step 3: Assemble the Crew
    # Process.sequential: Task 1 must finish before Task 2 starts
    # memory=False: disabled because it requires a hosted embedding service
    # verbose=True: prints detailed agent reasoning logs (useful for debugging)
    financial_crew = Crew(
        agents=[quant_agent, strategist_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        memory=False,
    )

    # Step 4: Start the analysis pipeline
    print(f"Kicking off Financial Analysis for {ticker}...")
    result = financial_crew.kickoff()

    # Convert CrewOutput object to plain string for downstream use
    return str(result)