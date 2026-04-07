# 🌍 AI Trip Planner — GCP Pipeline

An end-to-end AI-powered travel itinerary generator built with **LangChain**, **LangGraph**, and **Groq LLaMA 3.3**, designed to run on **Google Colab** and deployable as a **Streamlit** web application. The pipeline uses real-time web search (Tavily + Google Serper) to produce personalized, up-to-date travel plans for any destination.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Pipeline Stages](#pipeline-stages)
- [Prerequisites](#prerequisites)
- [Setup & Usage](#setup--usage)
- [API Keys](#api-keys)
- [Sample Queries](#sample-queries)
- [Outputs](#outputs)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Overview

This project implements a conversational AI travel planner that:

- Accepts user inputs such as destination, trip duration, interests, travel style, pace, and month of travel
- Invokes a **ReAct agent** (LangGraph) backed by Groq's `llama-3.3-70b-versatile` model
- Performs live web searches via **Tavily** and **Google Serper** to gather real-world, current travel data
- Synthesizes all gathered information into a structured, day-by-day itinerary
- Saves all outputs to disk and optionally serves them via a **Streamlit** frontend

The notebook (`AI_Trip_Planner_GCP_Pipeline_Final.ipynb`) mirrors the production project structure — every source file is written programmatically from within the notebook cells, making the entire codebase reproducible and self-contained.

---

## Architecture

```
User Input (City, Days, Interests, Style, Pace, Month)
        │
        ▼
  TravelPlanner (src/core/planner.py)
        │
        ▼
  ReAct Travel Agent (src/agents/travel_agent.py)
  ┌─────────────────────────────────────┐
  │  LLM: Groq llama-3.3-70b-versatile │
  │  (Fallback: OpenAI gpt-4o)          │
  │                                     │
  │  Tools:                             │
  │   ├─ Tavily Search                  │
  │   └─ Google Serper Search           │
  └─────────────────────────────────────┘
        │
        ▼
  Structured Itinerary Output
  (Console / Streamlit / outputs/ directory)
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM (Primary) | Groq `llama-3.3-70b-versatile` |
| LLM (Fallback) | OpenAI `gpt-4o` |
| Agent Framework | LangGraph (`create_react_agent`) |
| LLM Orchestration | LangChain |
| Search Tool 1 | Tavily Search API |
| Search Tool 2 | Google Serper API |
| Frontend | Streamlit |
| Runtime | Google Colab / Local Python |
| Packaging | `setuptools` |

---

## Project Structure

```
AI_Trip_Planner/
├── app.py                          # Streamlit web application
├── setup.py                        # Package setup
├── versions.py                     # Installed package version checker
├── requirements.txt                # Python dependencies
│
├── src/
│   ├── agents/
│   │   └── travel_agent.py         # ReAct agent with LLM + tools
│   ├── config/
│   │   └── config.py               # API key configuration
│   ├── core/
│   │   └── planner.py              # TravelPlanner class (main orchestrator)
│   ├── tools/
│   │   ├── tavily_tool.py          # Tavily search tool wrapper
│   │   └── serper_tool.py          # Google Serper search tool wrapper
│   └── utils/
│       ├── logger.py               # Rotating file logger
│       └── custom_exception.py     # Structured exception with traceback info
│
├── outputs/                        # Generated itineraries and test results
│   ├── stage6a_tavily_test.txt
│   ├── stage6b_serper_test.txt
│   ├── stage10a_query1_kasol.txt
│   ├── stage10b_query2_goa.txt
│   ├── stage10c_query3_rajasthan.txt
│   └── stage10d_pipeline_summary.json
│
└── logs/                           # Timestamped application logs
    └── log_YYYY-MM-DD.log
```

---

## Pipeline Stages

The notebook is organized into 11 sequential stages:

| Stage | Description |
|---|---|
| **0** | Load API keys from Colab Secrets (or manual fallback) |
| **1** | Install all required Python dependencies |
| **2** | Create the production project directory structure |
| **3** | Write `src/utils/` — logger and custom exception handler |
| **4** | Write `src/config/config.py` — centralized API key config |
| **5** | Write `src/tools/` — Tavily and Google Serper search wrappers |
| **6** | Test both search tools with a live query |
| **7** | Write `src/agents/travel_agent.py` — ReAct agent initialization |
| **8** | Write `src/core/planner.py` — `TravelPlanner` orchestration class |
| **9** | Write `app.py` (Streamlit UI), `setup.py`, and `versions.py` |
| **10** | Run 3 full end-to-end itinerary queries and save all outputs |
| **11** | Zip and download the entire project + outputs |

---

## Prerequisites

- Python 3.9 or higher
- A **Google Colab** environment (recommended) or a local Python environment
- API keys for the following services (see [API Keys](#api-keys)):
  - Groq
  - Tavily
  - Google Serper

---

## Setup & Usage

### Option 1 — Google Colab (Recommended)

1. Open the notebook in Google Colab.
2. Navigate to **Runtime → Secrets** and add your API keys:
   - `GROQ_API_KEY`
   - `TAVILY_API_KEY`
   - `SERPER_API_KEY`
3. Run all cells from top to bottom (**Runtime → Run All**).
4. At the end of Stage 11, the complete project will be zipped and downloaded automatically.

### Option 2 — Local Environment

```bash
# 1. Clone or download the project
git clone <your-repo-url>
cd AI_Trip_Planner

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export GROQ_API_KEY="your-groq-api-key"
export TAVILY_API_KEY="your-tavily-api-key"
export SERPER_API_KEY="your-serper-api-key"

# 5. Run the Streamlit app
streamlit run app.py
```

---

## API Keys

| Service | Purpose | Get Key |
|---|---|---|
| **Groq** | Primary LLM inference (free tier available) | [console.groq.com](https://console.groq.com) |
| **Tavily** | AI-optimized web search (free tier available) | [tavily.com](https://tavily.com) |
| **Google Serper** | Google Search results via API | [serper.dev](https://serper.dev) |
| **OpenAI** *(optional)* | Fallback LLM (`gpt-4o`) | [platform.openai.com](https://platform.openai.com) |

> **Note:** To switch from Groq to OpenAI as the primary LLM, set `USE_OPENAI = True` in `src/agents/travel_agent.py`.

---

## Sample Queries

The pipeline runs three built-in sample queries during Stage 10:

| # | Destination | Days | Style | Pace | Month |
|---|---|---|---|---|---|
| 1 | Kasol, Himachal Pradesh | 3 | Budget | Relaxed | May |
| 2 | Goa | 5 | Mid-range | Balanced | December |
| 3 | Rajasthan (Jaipur, Jodhpur, Udaipur) | 7 | Luxury | Packed | October |

### Using the `TravelPlanner` Programmatically

```python
from src.core.planner import TravelPlanner

planner = TravelPlanner()
itinerary = planner.create_itinerary(
    city="Manali",
    days=4,
    interests=["Skiing", "Adventure Sports", "Photography"],
    style="Mid-range",
    pace="Balanced",
    month="January"
)
print(itinerary)
```

---

## Outputs

All outputs are saved to the `outputs/` directory:

| File | Description |
|---|---|
| `stage6a_tavily_test.txt` | Raw Tavily API test result |
| `stage6b_serper_test.txt` | Raw Serper API test result |
| `stage10a_query1_kasol.txt` | Full Kasol itinerary |
| `stage10b_query2_goa.txt` | Full Goa itinerary |
| `stage10c_query3_rajasthan.txt` | Full Rajasthan itinerary |
| `stage10d_pipeline_summary.json` | JSON manifest of the full pipeline run |

Application logs are written daily to `logs/log_YYYY-MM-DD.log`.

---

## Configuration

### Switching the LLM

Edit `src/agents/travel_agent.py`:

```python
USE_OPENAI = False   # Set to True to use OpenAI gpt-4o instead of Groq
```

### Adjusting Search Depth

Edit `src/tools/tavily_tool.py`:

```python
TavilySearch(max_results=5, ...)   # Increase for more search results per query
```

---

## Troubleshooting

**API key not found**
Ensure keys are set either in Colab Secrets or as environment variables before running the notebook. The Stage 0 cell will print which keys are set and which are missing.

**Import errors after writing source files**
If you modify and re-run individual cells out of order, restart the Colab runtime and run all cells again from Stage 0.

**Groq rate limit errors**
Groq's free tier has rate limits. Wait a few seconds between large queries or switch to `USE_OPENAI = True` if you have an OpenAI key available.

**Serper or Tavily returning empty results**
Verify your API keys are valid and have remaining quota on their respective dashboards.

---

## License

This project is intended for educational and personal use. Refer to the terms of service of each third-party API (Groq, Tavily, Serper, OpenAI) for usage restrictions.
