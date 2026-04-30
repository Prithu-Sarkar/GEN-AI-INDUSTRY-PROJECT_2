"""
Crew Orchestration Module.

Rate-limit resilience applied here:
  - tenacity retry with exponential backoff: if Groq returns RateLimitError,
    the crew automatically waits 45 seconds and retries (up to 4 attempts).
    This handles transient spikes without requiring manual re-runs.
  - memory=False at Crew level: prevents hidden embedding API calls.
  - tracing disabled: removes LangSmith API overhead.
"""
import time
from crewai import Crew, Process
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log,
)
import logging
from src.agents.agents import create_agents
from src.agents.tasks import create_tasks

# Logger for tenacity retry messages
logger = logging.getLogger(__name__)


def _is_rate_limit_error(exc: Exception) -> bool:
    """
    Returns True if the exception is a Groq/LiteLLM rate limit error.

    Checks both the exception class name and the message string to handle
    the various ways LiteLLM surfaces rate limit errors.

    Args:
        exc: Any exception raised during crew execution.

    Returns:
        bool: True if this is a rate limit error that warrants a retry.
    """
    err_str = str(exc).lower()
    return (
        "rate_limit" in err_str
        or "ratelimit" in err_str
        or "rate limit" in err_str
        or "tokens per minute" in err_str
        or "tpm" in err_str
    )


def run_financial_crew(ticker: str) -> str:
    """
    Initialize and execute the Financial Analysis Crew with retry logic.

    Retry strategy:
        - Up to 4 attempts total.
        - Wait: 45s after attempt 1, 90s after attempt 2, 180s after attempt 3.
        - Only retries on rate limit errors; other errors propagate immediately.

    Args:
        ticker (str): Stock symbol to analyze (e.g. NVDA).

    Returns:
        str: Final Markdown investment report as a string.
    """
    quant_agent, strategist_agent = create_agents()
    tasks = create_tasks(quant_agent, strategist_agent, ticker)

    # Assemble the crew
    financial_crew = Crew(
        agents=[quant_agent, strategist_agent],
        tasks=tasks,
        process=Process.sequential,  # Quant must finish before Strategist starts
        verbose=True,
        memory=False,                # Disabled: embedding calls consume hidden TPM
    )

    attempt = 0
    max_attempts = 4
    # Wait schedule: 45s, 90s, 180s between retries
    wait_times = [45, 90, 180]

    while attempt < max_attempts:
        try:
            print(f"Starting Financial Analysis for {ticker} (attempt {attempt + 1}/{max_attempts})...")
            result = financial_crew.kickoff()
            return str(result)
        except Exception as e:
            if _is_rate_limit_error(e) and attempt < max_attempts - 1:
                wait = wait_times[attempt]
                # FIX: Removed leading newline from f-string literal
                print(f"[Rate Limit] Groq TPM exceeded. Waiting {wait}s before retry {attempt + 2}/{max_attempts}...")
                print(f"[Rate Limit] Error detail: {str(e)[:120]}")
                time.sleep(wait)
                attempt += 1
            else:
                # Non-rate-limit error or out of retries: propagate immediately
                raise

    raise RuntimeError(f"Crew failed after {max_attempts} attempts for ticker {ticker}.")