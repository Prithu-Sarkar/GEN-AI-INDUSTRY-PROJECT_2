"""
Financial Data Extraction Tools.

Two CrewAI BaseTool subclasses that give the Quantitative Analyst agent
access to live market data via the yfinance library:

  FundamentalAnalysisTool  -- snapshot metrics (P/E, Beta, EPS, Market Cap)
  CompareStocksTool        -- 1-year relative performance between two tickers
"""

from typing import Type, Dict, Any
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
import yfinance as yf


# ── Input Schemas ─────────────────────────────────────────────────────────────

class StockAnalysisInput(BaseModel):
    """Pydantic schema enforcing a single ticker string for FundamentalAnalysisTool."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g. AAPL, NVDA, MSFT).")


class CompareStocksInput(BaseModel):
    """Pydantic schema requiring two distinct tickers for CompareStocksTool."""
    ticker_a: str = Field(..., description="First stock ticker to analyze.")
    ticker_b: str = Field(..., description="Second stock ticker to compare against.")


# ── Tool Definitions ──────────────────────────────────────────────────────────

class FundamentalAnalysisTool(BaseTool):
    """
    CrewAI tool: fetches key fundamental financial metrics from Yahoo Finance.

    Returns a curated dictionary (as string) to avoid LLM context-window bloat.
    Only ~11 high-signal fields are extracted from the full ~100-key yfinance payload.
    """

    name: str = "Fetch Fundamental Metrics"
    description: str = (
        "Fetches key financial metrics for a specific stock ticker. "
        "Returns P/E Ratio, Beta, Market Cap, EPS, 52-week range, and analyst recommendation."
    )
    args_schema: Type[BaseModel] = StockAnalysisInput

    def _run(self, ticker: str) -> str:
        """
        Fetches fundamental data for a given stock symbol.

        Args:
            ticker (str): The stock symbol to look up (case-insensitive).

        Returns:
            str: Stringified dict of selected financial metrics,
                 or error message string on failure.
        """
        try:
            # Create Ticker object — no network call yet
            stock = yf.Ticker(ticker)

            # .info triggers the HTTP fetch from Yahoo Finance
            info: Dict[str, Any] = stock.info

            # Extract only the most diagnostically useful fields
            # .get() with default 'N/A' prevents KeyError on tickers with sparse data
            metrics = {
                "Ticker":                     ticker.upper(),
                "Current Price":              info.get("currentPrice", "N/A"),
                "Market Cap":                 info.get("marketCap", "N/A"),
                "P/E Ratio (Trailing)": info.get("trailingPE", "N/A"),
                "Forward P/E":                info.get("forwardPE", "N/A"),
                "PEG Ratio":                  info.get("pegRatio", "N/A"),
                "Beta (Volatility)":          info.get("beta", "N/A"),
                "EPS (Trailing)":             info.get("trailingEps", "N/A"),
                "52 Week High":               info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low":                info.get("fiftyTwoWeekLow", "N/A"),
                "Analyst Recommendation":     info.get("recommendationKey", "none"),
            }
            return str(metrics)

        except Exception as e:
            # Returning an error string (not raising) lets CrewAI retry gracefully
            return f"Error fetching fundamental data for '{ticker}': {str(e)}"


class CompareStocksTool(BaseTool):
    """
    CrewAI tool: calculates relative 1-year percentage performance between two assets.

    Typical use: compare a stock against SPY (S&P 500 ETF) to judge alpha.
    Formula: ((last_close - first_close) / first_close) * 100
    """

    name: str = "Compare Stock Performance"
    description: str = (
        "Compares historical performance of two stocks over the last 365 days. "
        "Returns the percentage gain or loss for both assets."
    )
    args_schema: Type[BaseModel] = CompareStocksInput

    def _run(self, ticker_a: str, ticker_b: str) -> str:
        """
        Downloads historical price data and computes percentage returns.

        Args:
            ticker_a (str): Symbol of the stock to analyze.
            ticker_b (str): Symbol of the benchmark (e.g. SPY).

        Returns:
            str: Formatted performance comparison string, or error message.
        """
        try:
            # Download the last year of closing prices for both tickers in one call
            # progress=False suppresses the tqdm download bar
            data = yf.download(
                f"{ticker_a} {ticker_b}",
                period="1y",
                progress=False,
                auto_adjust=True
            )["Close"]

            def calculate_return(symbol: str) -> float:
                """
                Computes percent change from the first to the last available close.

                Args:
                    symbol (str): Column name in the downloaded DataFrame.

                Returns:
                    float: Percentage return (e.g. 23.5 means +23.5%).
                """
                start_price = data[symbol].iloc[0]
                end_price = data[symbol].iloc[-1]
                return ((end_price - start_price) / start_price) * 100

            perf_a = calculate_return(ticker_a)
            perf_b = calculate_return(ticker_b)

            return f"""Performance Comparison (Last 1 Year):
  {ticker_a.upper()}: {perf_a:.2f}%
  {ticker_b.upper()}: {perf_b:.2f}%"""

        except Exception as e:
            return f"Error comparing stocks '{ticker_a}' vs '{ticker_b}': {str(e)}"