"""
Web Scraping and Sentiment Extraction Tool.

Integrates the Firecrawl API to give the Investment Strategist agent
real-time access to news, analyst ratings, and market commentary.

Unlike a basic Google Search (which returns only snippets), Firecrawl
visits the actual pages and converts them to clean Markdown, giving
the LLM richer context for qualitative reasoning.
"""

from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from src.shared.config import settings


# ── Input Schema ──────────────────────────────────────────────────────────────

class FirecrawlSearchInput(BaseModel):
    """Pydantic schema for the SentimentSearchTool requiring a search query string."""
    query: str = Field(
        ...,
        description="The search query (e.g. 'NVDA recent analyst ratings 2024')."
    )


# ── Tool Definition ───────────────────────────────────────────────────────────

class SentimentSearchTool(BaseTool):
    """
    CrewAI tool: searches the web for stock news and returns scraped content.

    Returns the top 3 results from Firecrawl as a Markdown-formatted string.
    Capped at 3 results to balance context window usage vs. information density.
    """

    name: str = "Search Stock News"
    description: str = (
        "Searches the web for the latest news, analyst ratings, and market sentiment "
        "surrounding a specific stock or financial topic. "
        "Returns a summary of the top 3 relevant articles."
    )
    args_schema: Type[BaseModel] = FirecrawlSearchInput

    def _run(self, query: str) -> str:
        """
        Executes a semantic search via the Firecrawl API.

        Args:
            query (str): The news topic or question to search for.

        Returns:
            str: Markdown-formatted scraped content from top search results,
                 or an error message string if the API call fails.
        """
        # Guard: Firecrawl SDK will raise an obscure error without the key
        if not settings.firecrawl_api_key:
            return "Error: FIRECRAWL_API_KEY is missing in configuration."

        try:
            # Lazy import to avoid package errors if not installed
            from firecrawl import FirecrawlApp

            # Initialize the Firecrawl client with our API key
            app = FirecrawlApp(api_key=settings.firecrawl_api_key)

            # Perform semantic search:
            # limit=3: only top 3 results to stay within LLM context budget
            # formats=["markdown"]: ensures clean text output (vs. raw HTML)
            results = app.search(
                query=query,
                limit=3,
                scrape_options={"formats": ["markdown"]}
            )

            # Truncate content of each result to reduce input size for the LLM
            truncated_results = []
            for res in results:
                if 'content' in res:
                    res['content'] = res['content'][:1000] + ('...' if len(res['content']) > 1000 else '')
                truncated_results.append(res)

            # Convert truncated result object to a readable string for the LLM
            return str(truncated_results)

        except Exception as e:
            return f"Error executing Firecrawl search for '{query}': {str(e)}"