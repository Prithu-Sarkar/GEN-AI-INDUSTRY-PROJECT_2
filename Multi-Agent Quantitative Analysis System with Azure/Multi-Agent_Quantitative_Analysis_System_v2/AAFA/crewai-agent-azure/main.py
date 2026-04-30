"""
CLI Entry Point.
Runs the Crew -> Uploads to Storage -> Saves to Database.
"""
import os, sys
from dotenv import load_dotenv
load_dotenv()

if not os.getenv("GROQ_API_KEY") or not os.getenv("FIRECRAWL_API_KEY"):
    print("Error: Missing GROQ_API_KEY or FIRECRAWL_API_KEY in .env")
    sys.exit(1)

from src.agents.crew import run_financial_crew
from src.shared.storage import StorageService
from src.shared.database import DatabaseService

def main():
    print("================================================")
    print("     AI Financial Analyst Crew (v2)            ")
    print("================================================")
    ticker = input("Enter a stock ticker (e.g. MSFT): ").strip().upper()
    if not ticker:
        return
    result_text = run_financial_crew(ticker)
    print(result_text)
    filename = f"investment_report_{ticker}.md"
    url = StorageService().upload_file(filename, filename)
    print(f"Report URL: {url}")
    DatabaseService().save_report(ticker=ticker, content=result_text)
    print("Pipeline complete.")

if __name__ == "__main__":
    main()