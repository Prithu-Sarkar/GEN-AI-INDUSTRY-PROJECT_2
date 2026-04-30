"""
Financial Data Extraction Tools.

Rate-limit resilience strategy:
  - FundamentalAnalysisTool returns ONLY the 8 highest-signal fields.
    Sending all 100+ yfinance keys would inflate the LLM context
    and consume the free-tier TPM budget unnecessarily.
  - CompareStocksTool returns a single-line result (minimal tokens).
"""
import time
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf


class StockAnalysisInput(BaseModel):
    """Input schema: a single stock ticker string."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g. AAPL, NVDA).")


class CompareStocksInput(BaseModel):
    """Input schema: two tickers for side-by-side comparison."""
    ticker_a: str = Field(..., description="First stock ticker.")
    ticker_b: str = Field(..., description="Benchmark ticker (e.g. SPY).")


class FundamentalAnalysisTool(BaseTool):
    """
    Fetches 8 key fundamental metrics from Yahoo Finance.

    Token budget rationale:
        A typical yfinance .info dict has 100+ keys (~2000 tokens if stringified).
        We return only 8 fields (~120 tokens). This single change cuts the
        Quant agent context by ~85% and is the most effective rate-limit fix.
    """
    name: str = "Fetch Fundamental Metrics"
    description: str = (
        "Fetches 8 key financial metrics for a stock: "
        "Price, Market Cap, P/E, Beta, EPS, 52w High/Low, Analyst Rating."
    )
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker: str) -> str:
        """
        Fetch and return a minimal, token-efficient metrics dict.

        Args:
            ticker (str): Stock symbol to analyze.

        Returns:
            str: Compact stringified dict with 8 key metrics only.
        """
        try:
            info: Dict[str, Any] = yf.Ticker(ticker).info

            # ONLY 8 fields — chosen for maximum analytical signal per token.
            # P/E + EPS = valuation. Beta = risk. Market Cap = size tier.
            # 52w range = momentum context. Analyst rec = consensus signal.
            metrics = {
                "Ticker":            ticker.upper(),
                "Price":             info.get("currentPrice", "N/A"),
                "MarketCap":         info.get("marketCap", "N/A"),
                "TrailingPE":        info.get("trailingPE", "N/A"),
                "Beta":              info.get("beta", "N/A"),
                "EPS":               info.get("trailingEps", "N/A"),
                "52wHigh":           info.get("fiftyTwoWeekHigh", "N/A"),
                "52wLow":            info.get("fiftyTwoWeekLow", "N/A"),
                "AnalystRec":        info.get("recommendationKey", "none"),
            }
            return str(metrics)
        except Exception as e:
            return f"Error fetching data for {ticker}: {e}"


class CompareStocksTool(BaseTool):
    """
    Computes 1-year relative performance between two tickers.

    Token budget: returns a 2-line string (~25 tokens). No tables, no prose.
    """
    name: str = "Compare Stock Performance"
    description: str = (
        "Returns the 1-year percentage return for two stocks. "
        "Use ticker_b=SPY to benchmark against the S&P 500."
    )
    args_schema: Type[BaseModel] = CompareStocksInput

    def _run(self, ticker_a: str, ticker_b: str) -> str:
        """
        Download closing prices and compute percentage return for each ticker.

        Returns a minimal 2-line summary to conserve LLM context tokens.
        """
        try:
            data = yf.download(
                f"{ticker_a} {ticker_b}",
                period="1y",
                progress=False,
                auto_adjust=True
            )["Close"]

            def pct(sym):
                """Calculate percentage return from first to last close."""
                return ((data[sym].iloc[-1] - data[sym].iloc[0]) / data[sym].iloc[0]) * 100

            # Single-line format: minimal tokens, same information density
            return f"{ticker_a.upper()}: {pct(ticker_a):.1f}% | {ticker_b.upper()}: {pct(ticker_b):.1f}% (1yr)"
        except Exception as e:
            return f"Error comparing {ticker_a} vs {ticker_b}: {e}"