"""
API Data Models.

Defines the Pydantic schemas for HTTP request and response bodies.
FastAPI uses these for automatic validation and OpenAPI documentation.
"""

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """
    Request body for POST /api/v1/analyze.

    Attributes:
        ticker (str): The stock symbol to analyze (e.g. NVDA, TSLA).
    """
    ticker: str = Field(..., description="The stock ticker symbol (e.g. NVDA, TSLA).")


class AnalysisResponse(BaseModel):
    """
    Response body returned after a successful analysis run.

    Attributes:
        status (str): "success" or "error".
        ticker (str): The analyzed stock symbol.
        report_content (str): Full Markdown text of the investment report.
        report_url (str): Azure blob URL or local file path of the saved report.
        message (str): Human-readable summary message.
    """
    status: str
    ticker: str
    report_content: str
    report_url: str
    message: str