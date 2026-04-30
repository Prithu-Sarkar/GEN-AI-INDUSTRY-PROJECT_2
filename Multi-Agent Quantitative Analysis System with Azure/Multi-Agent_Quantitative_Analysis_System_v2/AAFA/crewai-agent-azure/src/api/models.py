"""
API Data Models.
Pydantic schemas for FastAPI request/response validation and OpenAPI docs.
"""
from pydantic import BaseModel, Field

class AnalysisRequest(BaseModel):
    """POST /api/v1/analyze request body."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g. NVDA).")

class AnalysisResponse(BaseModel):
    """POST /api/v1/analyze response body."""
    status: str
    ticker: str
    report_content: str
    report_url: str
    message: str