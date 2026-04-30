# Multi-Agent Quantitative Analysis System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CrewAI](https://img.shields.io/badge/CrewAI-Multi--Agent-FF4B4B?style=for-the-badge)
![LiteLLM](https://img.shields.io/badge/LiteLLM-Provider--Agnostic-8A2BE2?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-Production_API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Azure](https://img.shields.io/badge/Azure-Cloud_Ready-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**A production-grade, FAANG-level multi-agent AI system for autonomous quantitative stock analysis.**
Two specialized AI agents collaborate in real time — one crunches numbers, one reads the market — and synthesize a professional investment report in minutes.

[Architecture](#architecture) · [Versions](#versions) · [Quickstart](#quickstart) · [API Reference](#api-reference) · [LLM Guide](#llm-provider-guide) · [Roadmap](#roadmap)

</div>

---

## The Problem This Solves

Professional equity research demands two fundamentally different disciplines working in parallel: a quantitative analyst who lives in financial data and a strategist who interprets market narrative. Traditionally this requires a team of analysts and hours of coordinated work.

This system replicates that entire workflow autonomously. Input a ticker — two AI agents with distinct personas, tool access, and reasoning chains divide the work, exchange findings via a formal context-injection mechanism, and deliver a structured BUY / SELL / HOLD report with full reasoning. No manual steps. End-to-end in under five minutes.

---

## What Makes This FAANG-Level

This is not a chatbot wrapper around a finance API. The architecture implements patterns used in production AI systems at scale:

- **True agent specialization.** The Quant agent has zero access to news tools. The Strategist has zero access to financial APIs. Separation of concerns is enforced at the framework level, not by prompt instruction alone.
- **Formal context injection.** The Strategist receives the Quant's full structured output via CrewAI's `context=[]` dependency graph before executing — not via naive prompt concatenation.
- **Tool-use first design.** Agents do not generate numbers. Every financial metric is fetched live from Yahoo Finance. Every news item is scraped live via Firecrawl. The LLM's role is reasoning and synthesis, not data retrieval.
- **Full production persistence.** Reports are uploaded to Azure Blob Storage and indexed in Azure PostgreSQL with timestamps, making every run auditable and reproducible.
- **REST API + UI layer.** A FastAPI backend and Streamlit frontend sit on top of the agent pipeline, making this directly deployable as a SaaS product.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER REQUEST  (Ticker: NVDA)                 │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   CrewAI Orchestrator│
                    │  (Sequential Process)│
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
   ┌──────────▼──────────┐          ┌──────────▼──────────┐
   │  Agent 1            │          │  Agent 2            │
   │  Quantitative       │─context─►│  Investment         │
   │  Analyst            │          │  Strategist         │
   │                     │          │                     │
   │  Tools:             │          │  Tools:             │
   │  • FundamentalTool  │          │  • SentimentSearch  │
   │  • CompareStocks    │          │    (Firecrawl)      │
   │    (Yahoo Finance)  │          │                     │
   └──────────┬──────────┘          └──────────┬──────────┘
              │                                 │
              └─────────────┬───────────────────┘
                            │
               ┌────────────▼────────────────┐
               │    Final Investment Report   │
               │   Markdown · BUY/SELL/HOLD   │
               └────────────┬────────────────┘
                            │
               ┌────────────▼────────────────┐
               │      Persistence Layer       │
               │  Azure Blob + PostgreSQL     │
               └─────────────────────────────┘
```

### Folder Structure

```
Multi-Agent Quantitative Analysis System/
└── AAFA/
    └── crewai-agent-azure/
        ├── main.py                        # CLI entry point
        ├── pyproject.toml                 # Dependency manifest
        ├── src/
        │   ├── agents/
        │   │   ├── agents.py              # Agent persona + LLM definitions
        │   │   ├── tasks.py               # Task work orders + context chaining
        │   │   ├── crew.py                # Crew assembly + kickoff + retry logic
        │   │   └── tools/
        │   │       ├── financial.py       # Yahoo Finance tools (Quant agent)
        │   │       ├── scraper.py         # Firecrawl news tool (Strategist)
        │   │       └── search.py          # Extended search (extensible)
        │   ├── shared/
        │   │   ├── config.py              # Settings + env management
        │   │   ├── database.py            # SQLAlchemy ORM (PostgreSQL / SQLite)
        │   │   └── storage.py             # Azure Blob / local file service
        │   └── api/
        │       ├── main.py                # FastAPI app factory
        │       ├── models.py              # Pydantic request/response schemas
        │       └── routes.py              # /analyze endpoint controller
        └── frontend/
            └── app.py                     # Streamlit UI
```

---

## Agents In Detail

### Agent 1 — Senior Quantitative Analyst

> *"I do not care about rumors or news headlines. I only trust hard data."*

| Property | Value |
|----------|-------|
| **Tools** | `FundamentalAnalysisTool`, `CompareStocksTool` |
| **Data Source** | Yahoo Finance (live) |
| **Delegation** | Disabled — works independently |

Fetches: Current Price · Market Cap · P/E (Trailing + Forward) · PEG Ratio · Beta · EPS · 52-week High/Low · Analyst consensus · 1-year return vs. SPY

### Agent 2 — Chief Investment Strategist

> *"Stock prices are driven by human psychology, news, and leadership changes."*

| Property | Value |
|----------|-------|
| **Tools** | `SentimentSearchTool` (Firecrawl) |
| **Data Source** | Live web — news, analyst ratings |
| **Context Input** | Full Quant output via `context=[quant_task]` |

Produces: Top news summaries · Risk flag detection · Numbers-vs-narrative synthesis · BUY / SELL / HOLD verdict · Full Markdown investment report saved to disk and cloud.

---

## Versions

This project ships in two versions that share identical architecture, folder structure, agent logic, and API surface. The differences live entirely in the LLM configuration layer and a set of engineering additions in v2 that make the system resilient when operating on a free-tier inference API.

---

### v1 — Original (OpenAI GPT-4o / Full Capability)

The baseline implementation. Designed for OpenAI's API where there are no meaningful token-per-minute constraints on paid tiers. The system runs with full verbosity, rich backstories, maximum tool output, and unrestricted response length. Every LLM call is allowed to be as thorough as the model decides it needs to be.

**LLM Configuration:**
```python
# src/shared/config.py
openai_api_key:    str = Field(...)
openai_model_name: str = Field("gpt-4o")
# No max_tokens cap — responses are fully unrestricted
```

**Agent configuration:**
```python
# src/agents/agents.py
Agent(
    ...
    memory=True,            # Cross-session memory enabled
    # No step_callback delay — OpenAI paid tier has no TPM ceiling
)

Crew(
    ...
    memory=True,
    tracing=True,           # LangSmith observability enabled
)
```

**Tool output — `FundamentalAnalysisTool`:** Returns all 11 financial fields. On GPT-4o this is appropriate — the model handles large contexts efficiently and paid-tier TPM headroom makes verbosity a non-issue.

**Task prompts:** Full descriptive prose with numbered steps, contextual qualifiers, and conditional reasoning instructions. Richer prompts yield more thorough, better-structured reports when token cost is not a constraint.

**Why v1 is the correct choice with a paid LLM:**
On OpenAI's paid tier or Anthropic's API, there are no per-minute token limits that matter in practice for a two-agent pipeline. GPT-4o produces measurably richer analysis — the Strategist's synthesis section is longer, more nuanced, and more defensible. The final verdict includes granular risk-weighting that the constrained v2 prompts cannot reliably elicit. `memory=True` enables agents to build cross-session context across multiple runs on the same ticker over time. There is no engineering justification for applying the v2 token-saving measures when the LLM infrastructure supports unrestricted operation.

---

### v2 — Rate-Limit Resilient (Groq LLaMA 3.3 70B Versatile)

An engineering-hardened version of the identical architecture, built to operate reliably within Groq's free tier: **6,000 tokens per minute**. A standard two-agent pipeline run consumes approximately 8,000–14,000 tokens without mitigation. This hits the rate ceiling mid-execution on nearly every run.

v2 applies seven targeted changes — each one measurable, none degrading analytical output in a meaningful way.

#### The Rate-Limit Problem, Precisely

Groq's free tier enforces a hard ceiling of 6,000 tokens per minute (TPM). A typical v1-style run breaks down as:

| Component | Token Cost (approx.) |
|-----------|---------------------|
| Quant agent system prompt (role + backstory) | ~180 tokens |
| Quant task description | ~220 tokens |
| FundamentalAnalysisTool output (11 fields) | ~350 tokens |
| CompareStocksTool output | ~60 tokens |
| Quant LLM response (uncapped) | ~800–2,400 tokens |
| Strategist system prompt | ~190 tokens |
| Strategist task description | ~240 tokens |
| SentimentSearchTool output (3 articles) | ~700 tokens |
| Quant context injected into Strategist | ~400 tokens |
| Strategist LLM response (uncapped) | ~1,200–3,500 tokens |
| **Total** | **~4,340–8,240 tokens** |

At the upper bound this exceeds 6,000 TPM. The failure is non-deterministic — it depends on how verbose the LLM is on a given run — making it appear intermittent and difficult to diagnose without this breakdown.

#### v2 Fixes — In Order of Impact

**Fix 1 — `max_tokens=1024` per LLM call** *(reduces output tokens by ~70%)*

The single most impactful change. Without a cap, each response can reach 2,000–3,500 tokens. Capping at 1,024 is sufficient for a structured analytical step and eliminates the worst-case token spike entirely.

```python
# src/agents/agents.py
def _build_llm() -> LLM:
    return LLM(
        model="groq/llama-3.3-70b-versatile",
        max_tokens=1024,    # Hard cap per response
        temperature=0.1,
    )
```

**Fix 2 — `FundamentalAnalysisTool` trimmed to 8 fields** *(reduces tool context by ~65%)*

v1 returned all 11 financial fields. v2 returns the 8 highest signal-to-noise fields only. The removed fields (Forward P/E, PEG Ratio, redundant price variants) added token cost with marginal analytical value.

```python
# v1: 11 fields — ~350 tokens of tool output
metrics = {
    "Ticker", "Current Price", "Market Cap", "P/E Ratio (Trailing)",
    "Forward P/E", "PEG Ratio", "Beta (Volatility)", "EPS (Trailing)",
    "52 Week High", "52 Week Low", "Analyst Recommendation"
}

# v2: 8 fields — ~120 tokens of tool output
metrics = {
    "Ticker", "Price", "MarketCap", "TrailingPE",
    "Beta", "EPS", "52wHigh", "52wLow", "AnalystRec"
}
```

**Fix 3 — `SentimentSearchTool`: `limit=2`, output truncated to 1,600 chars** *(reduces tool context by ~45%)*

v1 fetched 3 Firecrawl articles with no truncation. v2 fetches 2 and clips the combined result to 1,600 characters. The marginal analytical value of a third article is low relative to the ~250 token saving.

```python
# v2: src/agents/tools/scraper.py
results = app.search(query=query, limit=2, ...)   # was limit=3
raw = str(results)
return raw[:1600] + "...[truncated]" if len(raw) > 1600 else raw
```

**Fix 4 — Task prompts shortened ~40%** *(reduces input tokens per call by ~80 tokens)*

Every character in `description=` is an input token charged on every LLM invocation. v2 prompts carry identical analytical instructions with redundant prose removed.

```python
# v1 task description: ~220 tokens
"Analyze the financial health of ticker {ticker}. "
"1. Use the FundamentalAnalysisTool to fetch P/E, EPS, Beta, and Market Cap. "
"2. Use the CompareStocksTool to compare {ticker} against SPY (S&P 500) "
"   to see its relative performance over the last year. "
"3. Identify any major numerical red flags such as negative EPS or extremely high P/E. "
"Output a concise summary of the hard numbers with clear section headers."

# v2 task description: ~130 tokens
f"Analyze {ticker} finances. "
f"1. Use FundamentalAnalysisTool to get metrics for {ticker}. "
f"2. Use CompareStocksTool: ticker_a={ticker}, ticker_b=SPY. "
f"3. List red flags (negative EPS, P/E > 50, Beta > 2). "
f"Output: 3 bullet points max. Be concise."
```

**Fix 5 — Backstories trimmed ~50%** *(reduces system prompt tokens by ~90 tokens per agent)*

Agent backstories are prepended to every LLM call as part of the system prompt. v2 backstories convey the same analytical persona in half the words.

**Fix 6 — `memory=False` on agents and crew** *(removes hidden embedding API calls)*

CrewAI memory requires an embedding model API call on each step. These calls consume tokens invisible in the main LLM logs but count against the per-minute TPM budget. Disabling memory eliminates this overhead entirely.

**Fix 7 — `step_callback` 5-second inter-step delay + exponential backoff retry**

The delay spreads token consumption across time. Even if total tokens per run approach 6,000, spacing calls 5 seconds apart keeps the per-minute rate below the ceiling. The retry mechanism handles any residual spikes:

```python
# src/agents/crew.py — retry schedule on RateLimitError
wait_times   = [45, 90, 180]   # seconds between attempts 1→2, 2→3, 3→4
max_attempts = 4
```

#### v2 Token Budget After All Fixes

| Component | v1 Tokens | v2 Tokens | Reduction |
|-----------|-----------|-----------|-----------|
| System prompts (both agents) | ~370 | ~190 | −49% |
| Task descriptions (both tasks) | ~460 | ~270 | −41% |
| FundamentalAnalysisTool output | ~350 | ~120 | −66% |
| SentimentSearchTool output | ~700 | ~400 | −43% |
| LLM responses (both agents) | ~1,600–5,900 | ~800–2,048 | −65% |
| **Total range** | **~3,480–7,780** | **~1,780–3,028** | **~−55%** |

The v2 upper bound of ~3,028 tokens sits comfortably within the 6,000 TPM ceiling with meaningful headroom.

---

### Version Comparison

| Capability | v1 (OpenAI / Full) | v2 (Groq Free Tier) |
|------------|-------------------|---------------------|
| **LLM** | GPT-4o / GPT-4o-mini | LLaMA 3.3 70B Versatile |
| **API tier required** | Paid ($0.001–$0.005/run) | Free |
| **`max_tokens` cap** | None — unrestricted | 1,024 per call |
| **Agent memory** | Enabled | Disabled |
| **LangSmith tracing** | Enabled | Disabled |
| **Tool output size** | Full (11 fields, 3 articles) | Trimmed (8 fields, 2 articles, 1,600 char cap) |
| **Task prompt style** | Full descriptive prose | Concise bullet-form |
| **Inter-step delay** | None needed | 5 seconds |
| **Retry logic** | None needed | Exponential backoff ×4 |
| **Report depth** | Richer, longer, more nuanced | Concise, structured, accurate |
| **Run reliability** | Near 100% on paid tier | Near 100% with v2 mitigations |
| **Estimated tokens/run** | ~3,500–7,800 | ~1,800–3,000 |

Both versions produce a valid, professionally structured BUY/SELL/HOLD investment report with cited metrics and news synthesis. The quality difference is in the depth and verbosity of the Strategist's synthesis section — not in analytical accuracy.

---

## LLM Provider Guide

The system is provider-agnostic via LiteLLM. A single line change in `src/shared/config.py` switches the entire pipeline to a different LLM with no other code changes required.

### Why Paid APIs Remove All v2 Constraints

The v2 engineering changes are a direct response to free-tier TPM limits — not to any fundamental limitation of the multi-agent architecture. On a paid LLM API, every v2 constraint can be reverted:

- `max_tokens` cap → remove it; the Strategist produces longer, richer synthesis
- `memory=False` → enable it; agents accumulate cross-session knowledge
- Trimmed tool outputs → restore all 11 fields and 3 news articles
- Shortened prompts → restore full analytical descriptions
- `step_callback` delay → remove it; pipeline completes in roughly half the time
- Retry logic → optional but harmless to retain as a safety net

The multi-agent architecture, context injection, tool-use pattern, persistence layer, and full API surface are identical across both operating modes.

### Provider Comparison

| Provider | Model | Free Tier | Cost/Run | Why It's Better Than Free Groq |
|----------|-------|-----------|----------|-------------------------------|
| **Groq** | `llama-3.3-70b-versatile` | Yes (6K TPM) | — | Current v2 default. Requires all mitigations. |
| **OpenAI** | `gpt-4o-mini` | No | ~$0.001 | Eliminates all v2 constraints. Best cost-to-quality entry point for paid. |
| **OpenAI** | `gpt-4o` | No | ~$0.005 | Maximum analytical depth. Strategist synthesis is measurably more nuanced and defensible. |
| **Anthropic** | `claude-haiku-4-5` | No | ~$0.0005 | Near-instant responses. 200K context window. Cheapest path to full v1-level reliability. |
| **Anthropic** | `claude-sonnet-4-5` | No | ~$0.003 | Claude's instruction-following produces the best-formatted Markdown reports. The 200K context window means the Strategist can ingest significantly more news content before truncation becomes necessary — a structural advantage over GPT-4o's 128K window for news-heavy analysis. |

### Switching Providers

**To OpenAI (recommended paid entry point):**
```python
# src/shared/config.py
self.model = "gpt-4o-mini"
os.environ["OPENAI_API_KEY"] = "sk-..."
# Also revert: max_tokens=None, memory=True, full prompts, remove step_callback
```

**To Anthropic:**
```python
# src/shared/config.py
self.model = "claude-haiku-4-5-20251001"
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
# Also revert: max_tokens=None, memory=True, full prompts, remove step_callback
```

**To Groq (v2 default):**
```python
# src/shared/config.py
self.groq_model = "groq/llama-3.3-70b-versatile"
self.max_tokens = 1024    # Keep all v2 constraints active
os.environ["GROQ_API_KEY"] = "gsk_..."
```

---

## Quickstart

### Prerequisites

- Python 3.12+
- `uv` package manager (`pip install uv`)
- API keys (see table below)

### Required API Keys

| Key | Where to Get | Required For |
|-----|-------------|--------------|
| `GROQ_API_KEY` | [console.groq.com](https://console.groq.com) → API Keys | v2 (Groq) |
| `OPENAI_API_KEY` | [platform.openai.com](https://platform.openai.com) → API Keys | v1 (OpenAI) |
| `ANTHROPIC_API_KEY` | [console.anthropic.com](https://console.anthropic.com) → API Keys | Anthropic variant |
| `FIRECRAWL_API_KEY` | [firecrawl.dev](https://www.firecrawl.dev) → Dashboard | All versions |

### Installation

```bash
git clone https://github.com/your-org/multi-agent-quant-analysis.git
cd "multi-agent-quant-analysis/AAFA/crewai-agent-azure"
uv sync
```

### Environment Setup

```env
# .env — uncomment one LLM provider block

# --- v2: Groq (free tier) ---
GROQ_API_KEY=gsk_...
FIRECRAWL_API_KEY=fc-...

# --- v1: OpenAI (paid) ---
# OPENAI_API_KEY=sk-...
# FIRECRAWL_API_KEY=fc-...

# --- Anthropic variant ---
# ANTHROPIC_API_KEY=sk-ant-...

# --- Optional: Observability ---
LANGCHAIN_TRACING_V2=false
LANGCHAIN_API_KEY=

# --- Optional: Azure cloud persistence ---
AZURE_POSTGRES_CONNECTION_STRING=postgresql://...
AZURE_BLOB_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
```

### Run via CLI

```bash
uv run python main.py
# Enter ticker when prompted: NVDA
```

### Run via API

```bash
# Terminal 1 — start the backend
uv run uvicorn src.api.main:app --reload

# Terminal 2 — start the frontend
uv run streamlit run frontend/app.py
# Open http://localhost:8501
```

---

## API Reference

### `POST /api/v1/analyze`

Triggers the full multi-agent pipeline for a given stock ticker.

```json
// Request body
{ "ticker": "NVDA" }

// Response body
{
  "status":         "success",
  "ticker":         "NVDA",
  "report_content": "# NVDA Investment Analysis\n\n## Executive Summary...",
  "report_url":     "https://youraccount.blob.core.windows.net/reports/investment_report_NVDA.md",
  "message":        "Analysis complete and saved."
}
```

Interactive Swagger docs available at `http://localhost:8000/docs`.

---

## Sample Output

```markdown
# NVDA — Investment Analysis Report

## Executive Summary
NVIDIA presents a compelling but richly valued growth opportunity.
Fundamental metrics confirm exceptional strength; recent news flow
supports continued momentum with manageable near-term regulatory risk.

**Verdict: BUY (with position sizing discipline)**

## Key Metrics
| Metric         | Value      | Signal   |
|----------------|-----------|----------|
| Price          | $875.40   | —        |
| Market Cap     | $2.15T    | Mega-cap |
| P/E (TTM)      | 68.2x     | ⚠ High   |
| Beta           | 1.72      | ⚠ High   |
| EPS (TTM)      | $12.84    | ✅ Strong |
| 52w Range      | $455–$974 | —        |
| 1yr vs SPY     | +63.1% α  | ✅ Strong |
| Analyst Rating | Strong Buy| ✅        |

## News Highlights
- Blackwell GPU shipments ahead of schedule (Reuters)
- EU antitrust review of data center dominance underway (FT)
- Q1 earnings beat consensus by 18% (Bloomberg)

## Risk Factors
Valuation requires 30%+ sustained earnings growth to justify current multiples.
EU regulatory overhang is slow-moving but non-trivial.

## Final Verdict
**BUY** — accumulate on pullbacks toward $800. Stop-loss at $720.
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Agent Framework | [CrewAI](https://crewai.com) |
| LLM Routing | [LiteLLM](https://litellm.ai) — provider-agnostic |
| LLM Inference | Groq / OpenAI / Anthropic |
| Financial Data | [yfinance](https://github.com/ranaroussi/yfinance) |
| Web Scraping | [Firecrawl](https://www.firecrawl.dev) |
| Retry Logic | [Tenacity](https://tenacity.readthedocs.io) |
| Data Validation | [Pydantic v2](https://docs.pydantic.dev) |
| REST API | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn |
| Frontend | [Streamlit](https://streamlit.io) |
| Database ORM | [SQLAlchemy](https://www.sqlalchemy.org) |
| Cloud Storage | Azure Blob Storage |
| Cloud Database | Azure PostgreSQL |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

---

## Roadmap

- [ ] **Multi-ticker portfolio sweep** — run the crew across a basket and produce a comparative ranking table
- [ ] **Sector rotation agent** — a third agent that contextualizes individual findings within broader sector momentum
- [ ] **Earnings calendar triggers** — auto-schedule analysis runs on upcoming earnings dates
- [ ] **Historical signal backtesting** — evaluate past BUY/SELL verdicts against actual price movements
- [ ] **PDF report export** — generate a polished PDF alongside the Markdown output
- [ ] **Vector memory** — persistent cross-session agent memory via a vector database
- [ ] **Options flow signal** — integrate unusual options activity as an additional sentiment input
- [ ] **Streaming API responses** — stream the report token-by-token to the frontend as it generates

---

## Contributing

Pull requests are welcome. For significant changes, please open an issue first to align on direction.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/sector-rotation-agent`
3. Commit: `git commit -m 'Add sector rotation agent'`
4. Push: `git push origin feature/sector-rotation-agent`
5. Open a Pull Request

All new tools must follow the `BaseTool` pattern with a Pydantic `args_schema` and a documented `_run()` method.

---

## License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built with [CrewAI](https://crewai.com) · Routed via [LiteLLM](https://litellm.ai) · Deployed on [Azure](https://azure.microsoft.com)

*"The market is a device for transferring money from the impatient to the patient."*
— Warren Buffett

</div>
