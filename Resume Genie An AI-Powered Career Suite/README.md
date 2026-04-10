# 🧞 Resume Genie — AI-Powered Career Suite

> **Four AI career tools in one notebook:** Resume Evaluation · JD Matching · Cover Letter Generation · Conversational Career Coach

---

## Overview

Resume Genie is an end-to-end, industry-grade Jupyter notebook that combines LLM inference, LangChain orchestration, MLflow experiment tracking, and MongoDB persistence into a single cohesive career intelligence platform. Upload a resume PDF once and get instant, structured feedback across four specialized modules — all running natively in Google Colab with zero frontend setup.

---

## Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | **Resume Checker** | Standalone resume evaluation — score out of 100, strengths, weaknesses, skills inventory, and recommended next career steps |
| 2 | **Resume Scorer / JD Matcher** | Deep analysis of resume vs. a specific job description — ATS score, keyword gaps, match percentage, and industry-specific feedback |
| 3 | **Cover Letter Generator** | Generates a tailored, ready-to-send 300–450 word cover letter from your resume and target JD, with streaming output and auto-download |
| 4 | **AI Career Coach** | Multi-turn conversational coach grounded in your resume — interview prep, salary negotiation, skill gap advice, and more |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **LLM (Primary)** | GROQ `llama-3.1-8b-instant` |
| **LLM (Fallback)** | OpenAI `gpt-4o-mini` |
| **Orchestration** | LangChain (`langchain`, `langchain_groq`, `langchain_community`) |
| **PDF Parsing** | LangChain `PyPDFLoader` + `pypdf` |
| **Experiment Tracking** | MLflow + DagsHub |
| **Persistence** | MongoDB (Atlas or self-hosted) |
| **Environment** | Google Colab (no Streamlit / no frontend required) |

---

## Getting Started

### Prerequisites

- Google Colab account (free tier works)
- API keys for: **GROQ**, **MongoDB**, **DagsHub / MLflow**
- *(Optional)* OpenAI API key for the fallback model

### Setup

**1. Clone or open the notebook**
```bash
git clone https://github.com/your-username/resume-genie.git
```
Open `Resume_Genie.ipynb` in Google Colab.

**2. Add secrets to Colab**

Go to **Colab → Secrets** (🔑 key icon in the sidebar) and add:

| Secret Name | Description |
|-------------|-------------|
| `GROQ_API_KEY` | Your GROQ API key |
| `MONGO_DB_URL` | MongoDB connection string |
| `MLFLOW_TRACKING_URI` | DagsHub MLflow URI |
| `MLFLOW_TRACKING_USERNAME` | DagsHub username |
| `MLFLOW_TRACKING_PASSWORD` | DagsHub token/password |

**3. Run all setup cells** (Cells 0–5) to install dependencies and initialize connections.

**4. Run any module** independently or use the **Full Pipeline Demo** cell to execute all four in sequence on a single PDF upload.

---

## Project Structure

```
Resume_Genie.ipynb
│
├── Cell 0   — Environment setup & secrets
├── Cell 1   — Dependency installation
├── Cell 2   — Imports & shared utilities
├── Cell 3   — LLM factory (GROQ primary / OpenAI fallback)
├── Cell 4   — MLflow / DagsHub + MongoDB initialization
├── Cell 5   — PDF parsing utilities
├── Cell 6   — Prompt templates (all 4 modules)
│
├── Module 1 — Resume Checker
├── Module 2 — Resume Scorer / JD Matcher
├── Module 3 — Cover Letter Generator
├── Module 4 — AI Career Coach (multi-turn chatbot)
│
├── Full Pipeline Demo — All 4 modules in one run
└── Analytics — MLflow run viewer + MongoDB query
```

---

## How Upgrading to Claude (Anthropic) Would Make This Better

Resume Genie currently uses GROQ's `llama-3.1-8b-instant` for fast, free-tier inference. Swapping in **Claude** (via the Anthropic API) or a **Pean AI** routing layer would meaningfully improve the quality of every module:

### 1. Dramatically Better Resume Analysis (Modules 1 & 2)

Claude models — particularly **Claude Opus** or **Claude Sonnet** — excel at long-context comprehension, structured output generation, and nuanced reasoning. For resume evaluation this means:

- More accurate ATS scoring with consistent section-by-section rubric application
- Richer, more specific career advice grounded in actual resume evidence rather than generic patterns
- Better handling of multi-page, dense, or unconventionally formatted CVs that smaller models parse poorly

### 2. Higher Quality Cover Letters (Module 3)

Cover letter generation requires blending two long documents (resume + JD) into natural, persuasive prose without hallucinating experience. Claude's superior instruction-following and tone control produce letters that:

- Match the JD's language and seniority level more accurately
- Sound human and personalized rather than template-generated
- Strictly avoid fabricating experience — a known failure mode of smaller models

### 3. A More Capable Career Coach (Module 4)

The multi-turn chatbot benefits the most from an upgrade. Claude's extended context window (up to 200K tokens in Claude 3.5 and beyond) means the coach can hold the **entire resume, the full conversation history, and deep persona instructions** in a single context — something the 8K-token `llama-3.1-8b-instant` cannot do. This enables:

- Sustained, coherent multi-turn coaching sessions without context truncation
- Remembering earlier parts of the conversation to give consistent advice
- Handling complex, multi-part interview prep sequences without losing thread

### 4. Safer, More Reliable Structured Output

LangChain chains that depend on structured output formats (scores, bullet lists, section headings) break when smaller models deviate from the requested format. Claude's strong instruction adherence significantly reduces parsing failures in `parse_score_from_output()` and the JD matcher's metric extraction regexes.

### How to Swap In Claude

```python
# pip install langchain_anthropic

from langchain_anthropic import ChatAnthropic

def get_llm(temperature: float = 0.2, max_tokens: int = 2000):
    return ChatAnthropic(
        model="claude-opus-4-5",          # or claude-sonnet-4-5 for faster/cheaper
        api_key=os.environ["ANTHROPIC_API_KEY"],
        temperature=temperature,
        max_tokens=max_tokens,
    )
```

Add `ANTHROPIC_API_KEY` to your Colab secrets and change `LLM_PROVIDER = "anthropic"` in the factory cell. No other code changes are required — every LangChain chain, prompt template, and streaming loop works identically.

---

## MLflow Experiment Tracking

Every tool invocation is logged to the `resume_genie_suite` MLflow experiment with:

- Parameters: `tool`, `llm`, `model`
- Metrics: `score`, `latency_sec`, `ats_score`, `match_pct`, `output_chars`
- Artifacts: raw LLM output text per run

View experiments at your DagsHub repo or run the **Analytics** cell at the bottom of the notebook.

---

## MongoDB Collections

| Collection | Contents |
|------------|----------|
| `resume_runs` | One document per tool invocation (metadata, inputs, output, metrics) |
| `resume_texts` | Cached extracted PDF texts (avoids re-parsing on re-runs) |
| `chat_sessions` | Full multi-turn career coach conversation logs per session |

---

## Environment Variables Reference

```
GROQ_API_KEY               — GROQ inference API key
OPENAI_API_KEY             — (Optional) OpenAI fallback key
ANTHROPIC_API_KEY          — (Optional) Claude / Anthropic API key
MONGO_DB_URL               — MongoDB Atlas connection string
MLFLOW_TRACKING_URI        — DagsHub or local MLflow URI
MLFLOW_TRACKING_USERNAME   — DagsHub username
MLFLOW_TRACKING_PASSWORD   — DagsHub access token
```

---

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you'd like to change.

---

## License

[MIT](LICENSE)
