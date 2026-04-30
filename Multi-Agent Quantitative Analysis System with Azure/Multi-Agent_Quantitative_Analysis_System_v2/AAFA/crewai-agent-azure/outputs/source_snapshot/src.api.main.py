"""
FastAPI Application Entry Point.
Run locally: uvicorn src.api.main:app --reload
"""
from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(
    title="CrewAI Financial Analyst API",
    description="Multi-Agent Stock Analysis powered by Groq LLaMA.",
    version="2.0.0",
)
app.include_router(router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "Financial Analyst Crew v2"}