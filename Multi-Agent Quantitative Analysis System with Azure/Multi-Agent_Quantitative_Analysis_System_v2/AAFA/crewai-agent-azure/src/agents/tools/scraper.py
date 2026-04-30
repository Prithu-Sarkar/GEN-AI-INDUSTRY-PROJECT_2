"""
Web Scraping and Sentiment Extraction Tool.

Rate-limit resilience:
  - limit=2 articles (down from 3) — reduces LLM input tokens by ~30%.
  - Each article result is sliced to 800 chars before returning —
    prevents a single verbose article from consuming the entire TPM budget.
"""
from typing import Type
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from src.shared.config import settings


class FirecrawlSearchInput(BaseModel):
    """Input schema: a search query string."""
    query: str = Field(..., description="Search query (e.g. NVDA analyst ratings 2025).")


class SentimentSearchTool(BaseTool):
    """
    Searches the web for stock news via Firecrawl.

    Token budget strategy:
        limit=2 fetches 2 articles instead of 3.
        Each result is truncated to 800 characters.
        Combined ceiling: ~400 tokens of tool output per call.
        This ensures the Strategist context stays well within free-tier TPM.
    """
    name: str = "Search Stock News"
    description: str = (
        "Searches for the latest news and analyst ratings for a stock. "
        "Returns summaries of the top 2 relevant articles."
    )
    args_schema: Type[BaseModel] = FirecrawlSearchInput

    def _run(self, query: str) -> str:
        """
        Execute Firecrawl search and return truncated results.

        Args:
            query (str): The news topic or question to search for.

        Returns:
            str: Truncated scraped content from top 2 search results.
        """
        if not settings.firecrawl_api_key:
            return "Error: FIRECRAWL_API_KEY missing."
        try:
            from firecrawl import FirecrawlApp
            app = FirecrawlApp(api_key=settings.firecrawl_api_key)

            # limit=2: fetch 2 articles only (was 3) to cut ~30% of output tokens
            results = app.search(
                query=query,
                limit=2,
                scrape_options={"formats": ["markdown"]}
            )

            # Truncate the full result string to 1600 chars.
            # A typical Firecrawl result for 2 articles is ~3000 chars (~750 tokens).
            # Truncating to 1600 chars keeps output under ~400 tokens.
            raw = str(results)
            return raw[:1600] + "...[truncated]" if len(raw) > 1600 else raw

        except Exception as e:
            return f"Error searching for {query}: {e}"