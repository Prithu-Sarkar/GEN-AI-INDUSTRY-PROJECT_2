# 🤖 AutoGen Data Analyzer GPT

> **An AI-powered, agentic data analysis system** built with Microsoft AutoGen v0.4 — drop in a CSV, ask questions in plain English, and get automated Python analysis with visualizations.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![AutoGen](https://img.shields.io/badge/AutoGen-v0.4-orange)](https://github.com/microsoft/autogen)
[![Groq](https://img.shields.io/badge/LLM-Groq%20%7C%20OpenAI-green)](https://groq.com)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

---

## 📖 Overview

AutoGen Data Analyzer GPT is a multi-agent pipeline that accepts any CSV file and a natural language question, then autonomously writes, executes, and iterates Python code to produce a complete data analysis with charts and insights — all without manual coding.

The system is powered by two cooperating agents in a `RoundRobinGroupChat` loop:

| Agent | Role |
|---|---|
| **Data Analyzer Agent** | LLM-backed agent (Groq / OpenAI) — interprets the user query, writes Python/bash analysis code |
| **Code Executor Agent** | Executes the generated code in a sandboxed local environment, returns results back to the loop |

The loop repeats until the analysis is complete (`STOP` keyword) or the maximum turn limit is reached, then saves all outputs (text + charts) to the `temp/` directory.

---

## 🏗️ Architecture

```text
User Query (natural language about CSV data)
        │
        ▼
  RoundRobinGroupChat  ──────────────────────────────────────┐
  │                                                           │
  │  Turn 1 → Data_Analyzer_Agent (LLM: Groq / OpenAI)       │
  │           • Reads user query + CSV context                │
  │           • Writes Python analysis code                   │
  │                                                           │
  │  Turn 2 → CodeExecutor_Agent                             │
  │           • Runs code via LocalCommandLineCodeExecutor    │
  │           • Returns stdout / errors to the chat           │
  │                                                           │
  │  Repeat ↑ until "STOP" signal or max_turns reached        │
  └───────────────────────────────────────────────────────────┘
        │
        ▼
  Output: analysis text + output.png saved to temp/
```

### Project Structure

```
AutoGen_Data_Analyzer/
├── src/
│   ├── agents/
│   │   ├── prompts/
│   │   │   └── DataAnalyzerAgentPrompt.py   # System prompt for LLM agent
│   │   ├── Data_analyzer_agent.py           # AssistantAgent definition
│   │   └── Code_Executor_agent.py           # CodeExecutorAgent definition
│   ├── config/
│   │   ├── constants.py                     # Global settings (turns, timeout, models)
│   │   ├── groq_model_client.py             # Groq LLM client (llama-3.3-70b)
│   │   └── openai_model_client.py           # OpenAI LLM client (gpt-4o)
│   ├── team/
│   │   └── analyzer_gpt.py                  # RoundRobinGroupChat team assembly
│   └── utils/
│       ├── logger.py                        # File-based logging
│       └── custom_exception.py             # Structured error reporting
├── temp/                                    # CSV input + generated outputs land here
├── main.py                                  # Entry point
├── setup.py
└── requirements.txt
```

---

## ✨ Features

- **Natural language querying** — ask any question about your CSV data in plain English
- **Fully agentic loop** — agents plan, write, execute, and self-correct code autonomously
- **No Docker required** — uses `LocalCommandLineCodeExecutor` (works in Colab and local environments)
- **Dual LLM support** — Groq `llama-3.3-70b-versatile` (free, fast) or OpenAI `gpt-4o` (fallback)
- **Auto-generated charts** — matplotlib/seaborn visualizations saved as `output.png`
- **Structured logging** — date-stamped log files in `logs/`
- **Modular codebase** — clean separation of agents, config, and utilities

---

## 🚀 Quick Start

### Option A — Google Colab (Recommended)

1. Open the notebook in Colab:  
   [![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com)

2. Add your API keys via **Runtime → Secrets**:
   - `GROQ_API_KEY` (get one free at [console.groq.com](https://console.groq.com))
   - `OPENAI_API_KEY` (optional fallback)

3. Run all cells top-to-bottom — the notebook scaffolds the entire project, uploads your CSV, and streams the analysis.

### Option B — Local Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/autogen-data-analyzer-gpt.git
cd autogen-data-analyzer-gpt

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set API keys
export GROQ_API_KEY="your-groq-api-key"
export OPENAI_API_KEY="your-openai-api-key"   # optional

# 5. Drop your CSV into temp/
cp your_data.csv temp/data.csv

# 6. Run the pipeline
python main.py
```

---

## ⚙️ Configuration

All global settings live in `src/config/constants.py`:

| Constant | Default | Description |
|---|---|---|
| `WORK_DIR` | `"temp"` | Working directory for code execution and outputs |
| `TIMEOUT_EXEC` | `120` | Max seconds allowed per code execution block |
| `MAX_TURNS` | `15` | Maximum agent conversation rounds |
| `TERMINATION_KW` | `"STOP"` | Keyword that signals the analysis is complete |
| `GROQ_MODEL` | `"llama-3.3-70b-versatile"` | Groq model identifier |
| `OPENAI_MODEL` | `"gpt-4o"` | OpenAI model identifier |
| `TEMPERATURE` | `0.3` | LLM sampling temperature |

To switch between Groq and OpenAI, set `USE_GROQ = False` in the pipeline cell (or `main.py`).

---

## 📦 Dependencies

```
autogen-agentchat
autogen-core
autogen-ext[openai]
autogen-ext[local]
groq
openai
tiktoken
python-dotenv
pandas
matplotlib
seaborn
```

Install everything with:
```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys

| Provider | Required | Get One |
|---|---|---|
| **Groq** | ✅ Primary | [console.groq.com](https://console.groq.com) — free tier available |
| **OpenAI** | ⚠️ Fallback | [platform.openai.com](https://platform.openai.com) |

Store keys in a `.env` file (local) or Colab Secrets (Colab). **Never commit API keys to version control.**

```env
# .env
GROQ_API_KEY=your-groq-key-here
OPENAI_API_KEY=your-openai-key-here
```

---

## 📋 Pipeline Stages

The Colab notebook walks through 10 clearly labelled stages:

| Stage | What Happens |
|---|---|
| **0** | Load API keys from Colab Secrets or environment |
| **1** | Install all pip dependencies |
| **2** | Scaffold the project directory structure |
| **3** | Write `src/utils/` — logger and custom exception handler |
| **4** | Write `src/config/` — constants and model clients |
| **5** | Write the Data Analyzer Agent system prompt |
| **6** | Write both agent definitions (DataAnalyzer + CodeExecutor) |
| **7** | Assemble the RoundRobinGroupChat team |
| **8** | Write `main.py`, `setup.py`, and `requirements.txt` |
| **9** | Upload CSV and run the full analysis pipeline |
| **10** | Display outputs and download a zip of all generated files |

---

## 🖥️ Example Usage

```python
from src.team.analyzer_gpt import run_analysis

# Ask any question about your CSV
await run_analysis(
    csv_path="temp/data.csv",
    query="What are the top 5 products by revenue? Plot a bar chart."
)
```

The agents will autonomously generate and execute the code, producing both a printed summary and a saved chart in `temp/output.png`.

---

## 📁 Outputs

All generated artifacts are saved to `temp/`:

```
temp/
├── data.csv          # Your input file
├── output.png        # Generated visualization(s)
└── ...               # Any additional files the agent produces
```

Logs are written to date-stamped files in `logs/`:
```
logs/
└── log_2025-01-15.log
```

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "Add my feature"`
4. Push and open a Pull Request

Please open an issue first for major changes so we can discuss the approach.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- [Microsoft AutoGen](https://github.com/microsoft/autogen) — multi-agent conversation framework
- [Groq](https://groq.com) — ultra-fast LLM inference API
- [OpenAI](https://openai.com) — GPT-4o fallback model

---

<div align="center">
  Built with ❤️ using AutoGen · Groq · OpenAI
</div>
