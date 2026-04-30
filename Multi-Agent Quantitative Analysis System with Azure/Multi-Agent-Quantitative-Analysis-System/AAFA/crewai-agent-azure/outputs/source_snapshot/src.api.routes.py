"""
API Routes.

Defines the /analyze endpoint that triggers the multi-agent pipeline.
Acts as the Controller layer: receives HTTP request, delegates to agents,
stores results in cloud, and returns structured JSON response.
"""

from fastapi import APIRouter, HTTPException
from src.api.models import AnalysisRequest, AnalysisResponse
from src.agents.crew import run_financial_crew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService

# APIRouter groups related endpoints under a common prefix
router = APIRouter()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """
    POST /api/v1/analyze

    Triggers the full Financial Analysis Crew pipeline:
      1. Runs the multi-agent AI crew.
      2. Uploads the report to Azure Blob Storage (or local fallback).
      3. Saves a record to the PostgreSQL database (or local SQLite).
      4. Returns the structured JSON response.

    Args:
        request (AnalysisRequest): JSON body containing the ticker symbol.

    Returns:
        AnalysisResponse: Full report content plus metadata.

    Raises:
        HTTPException 500: If any step in the pipeline fails.
    """
    ticker = request.ticker.upper()

    try:
        # Step 1: Run the AI crew and capture the Markdown report string
        print(f"API Request received for: {ticker}")
        report_text = run_financial_crew(ticker)

        # Step 2: Persist the report file to storage
        filename = f"investment_report_{ticker}.md"
        storage = StorageService()
        blob_url = storage.upload_file(filename, filename)

        # Step 3: Save metadata record to database
        db = DatabaseService()
        db.save_report(ticker=ticker, content=report_text)

        return AnalysisResponse(
            status="success",
            ticker=ticker,
            report_content=report_text,
            report_url=blob_url,
            message="Analysis complete and saved.",
        )

    except Exception as e:
        print(f"API Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))