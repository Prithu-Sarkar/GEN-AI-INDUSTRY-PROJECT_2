"""
API Routes.
Wires HTTP requests to the multi-agent pipeline.
"""
from fastapi import APIRouter, HTTPException
from src.api.models import AnalysisRequest, AnalysisResponse
from src.agents.crew import run_financial_crew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService

router = APIRouter()

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest):
    """
    POST /api/v1/analyze
    Triggers the crew pipeline, stores the report, returns structured JSON.
    """
    ticker = request.ticker.upper()
    try:
        report_text = run_financial_crew(ticker)
        filename = f"investment_report_{ticker}.md"
        blob_url = StorageService().upload_file(filename, filename)
        DatabaseService().save_report(ticker=ticker, content=report_text)
        return AnalysisResponse(
            status="success", ticker=ticker,
            report_content=report_text, report_url=blob_url,
            message="Analysis complete."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))