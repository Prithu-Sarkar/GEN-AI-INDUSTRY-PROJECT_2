"""
FastAPI Application Entry Point.

Wires the router into a FastAPI app instance.
To run locally: uvicorn src.api.main:app --reload
"""

from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="CrewAI Financial Analyst API",
    description="A Multi-Agent Agentic API for Stock Analysis powered by Groq LLaMA.",
    version="1.0.0",
)

# Mount analysis routes under /api/v1 prefix
app.include_router(router, prefix="/api/v1")


@app.get("/")
def health_check():
    """Root endpoint: confirms the service is reachable."""
    return {"status": "healthy", "service": "Financial Analyst Crew"}