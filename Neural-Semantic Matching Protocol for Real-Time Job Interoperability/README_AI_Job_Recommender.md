# 📄 AI Job Recommender

> An end-to-end AI-powered resume analyzer and job recommendation system using **OpenAI GPT-4o**, **Apify web scrapers**, **Streamlit**, and **MCP (Model Context Protocol)**.

---

## 🚀 Project Overview

The **AI Job Recommender** is a production-ready GenAI application that takes your resume (PDF), analyzes it using GPT-4o, and returns:

- ✅ A structured **resume summary**
- ✅ **Skill gap analysis** with actionable insights
- ✅ A personalized **career roadmap**
- ✅ Live **job recommendations** from **LinkedIn** and **Naukri** (India) via Apify scrapers

The project also exposes a **MCP (Model Context Protocol) tool server**, making it compatible with agentic AI workflows and Claude Desktop.

---

## 🏗️ Project Structure

```
AI-Job-Recommender/
│
├── app.py                         # Streamlit frontend application
├── mcp_server.py                  # MCP tool server (agentic AI integration)
├── requirements.txt               # Python dependencies
├── pyproject.toml                 # Project metadata (uv/pip)
├── .python-version                # Python version pin (3.13)
├── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── helper.py                  # PDF extraction + OpenAI GPT-4o calls
│   └── job_api.py                 # Apify scrapers for LinkedIn & Naukri
│
└── outputs/                       # Pipeline outputs (Colab run artifacts)
    ├── stage1_resume_text.txt
    ├── stage2_summary.txt
    ├── stage3_skill_gaps.txt
    ├── stage4_roadmap.txt
    ├── stage5_keywords.txt
    ├── stage6_linkedin_jobs.json
    └── stage7_naukri_jobs.json
```

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | OpenAI GPT-4o |
| **PDF Parsing** | PyMuPDF (`fitz`) |
| **Job Scraping** | Apify (LinkedIn + Naukri actors) |
| **Frontend** | Streamlit |
| **Agentic Tools** | MCP (`fastmcp`) |
| **Environment** | `python-dotenv` |
| **Runtime** | Python 3.13 |
| **Package Manager** | `uv` / `pip` |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name/AI-Job-Recommender
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv sync
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-openai-api-key
APIFY_API_TOKEN=your-apify-api-token
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

---

## 🖥️ Running the Streamlit App

```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

### App Workflow

1. Upload your **PDF resume**
2. The app extracts text and calls GPT-4o for:
   - Resume Summary
   - Skill Gap Analysis
   - Career Roadmap
3. Click **"Get Job Recommendations"** to fetch live jobs from LinkedIn and Naukri

---

## 🔌 MCP Tool Server

The `mcp_server.py` exposes two tools for agentic AI systems (e.g., Claude Desktop):

| Tool | Description |
|---|---|
| `fetchlinkedin(listofkey)` | Fetch LinkedIn jobs for given keywords |
| `fetchnaukri(listofkey)` | Fetch Naukri jobs for given keywords |

### Run the MCP Server

```bash
python mcp_server.py
```

### Integrate with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "job-recommender": {
      "command": "python",
      "args": ["path/to/mcp_server.py"]
    }
  }
}
```

---

## 📓 Google Colab Pipeline

A full end-to-end Colab notebook `AI_Job_Recommender_Pipeline.ipynb` is included for running the complete pipeline without a local setup.

### Colab Stages

| Stage | Description | Output |
|---|---|---|
| 0 | Set API keys | — |
| 1 | Install dependencies | — |
| 2 | Create project structure | `src/`, `outputs/` |
| 3 | Write `src/helper.py` | Helper module |
| 4 | Write `src/job_api.py` | Job API module |
| 5 | Write `mcp_server.py` | MCP server |
| 6 | Write `app.py` | Streamlit app |
| 7a | Upload & extract PDF resume | `stage1_resume_text.txt` |
| 7b | GPT-4o resume summary | `stage2_summary.txt` |
| 7c | Skill gap analysis | `stage3_skill_gaps.txt` |
| 7d | Career roadmap | `stage4_roadmap.txt` |
| 7e | Extract job keywords | `stage5_keywords.txt` |
| 7f | Fetch LinkedIn jobs | `stage6_linkedin_jobs.json` |
| 7g | Fetch Naukri jobs | `stage7_naukri_jobs.json` |
| 8 | Write `requirements.txt` + `README.md` | Project files |
| 9 | Zip & download all outputs | `AI_Job_Recommender_Outputs.zip` |

---

## 🔑 API Keys Required

### OpenAI
- Sign up at [platform.openai.com](https://platform.openai.com)
- Create an API key under **API Keys**
- Model used: `gpt-4o`

### Apify
- Sign up at [apify.com](https://apify.com)
- Get your token from **Settings → Integrations**
- Actors used:
  - `BHzefUZlZRKWxkTck` — LinkedIn Jobs Scraper
  - `alpcnRV9YI9lYVPWk` — Naukri Jobs Scraper

---

## 📦 Dependencies

```
streamlit
openai
pymupdf
python-dotenv
apify-client
mcp[cli]
```

---

## 🛡️ Security Notes

- `.env` is excluded via `.gitignore` — API keys are never committed
- All secrets are loaded via `python-dotenv` at runtime
- GitHub Push Protection will block any accidental secret commits

---

## 🙋 Author

**Prithu Sarkar**  
IIT Guwahati — MLOps & GenAI Industry Projects  
GitHub: [@Prithu-Sarkar](https://github.com/Prithu-Sarkar)

---

## 📄 License

This project is for educational and portfolio purposes as part of the IIT Guwahati GenAI Industry Project curriculum.
