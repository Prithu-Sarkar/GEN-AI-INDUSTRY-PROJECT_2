<div align="center">

# 🏥 End-to-End Medical Chatbot

### Retrieval-Augmented Generation · LangChain ≥ 1.2 · Groq Llama · ChromaDB

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-≥%201.2-1C3C3C?style=for-the-badge&logo=chainlink&logoColor=white)](https://python.langchain.com/)
[![Groq](https://img.shields.io/badge/Groq-Llama%203.1-F55036?style=for-the-badge&logo=meta&logoColor=white)](https://console.groq.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Free%20VectorDB-FF6B35?style=for-the-badge)](https://www.trychroma.com/)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-MiniLM%20384d-FFD21F?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge)](LICENSE)

<br/>

*A production-grade, fully open-source medical question-answering system powered by Retrieval-Augmented Generation. Ingest any medical PDF, embed it locally, and query it through a fast LLM — with zero paid vector database dependency.*

<br/>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Project Structure](#-project-structure)
- [Technology Stack](#-technology-stack)
- [LangChain 1.2+ — Import Changes & Compatibility](#-langchain-12--import-changes--compatibility)
- [Swapping the Data Source — What Changes](#-swapping-the-data-source--what-changes)
- [Environment Setup](#-environment-setup)
- [Running the Pipeline](#-running-the-pipeline)
- [Token Limit Strategy](#-token-limit-strategy)
- [Configuration Reference](#-configuration-reference)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🔭 Overview

The **End-to-End Medical Chatbot** is a RAG (Retrieval-Augmented Generation) system that transforms static medical PDF documents into an intelligent, conversational knowledge base. It is designed around three core principles:

| Principle | Implementation |
|-----------|---------------|
| **Zero paid infrastructure** | ChromaDB (local), HuggingFace embeddings (free), Groq free tier |
| **Accuracy over creativity** | Low temperature (0.2), context-grounded prompts, concise 3-sentence limit |
| **Maintainable codebase** | Clean `src/` separation of concerns, LangChain ≥ 1.2 modern API throughout |

The system ingests PDF documents, splits and embeds them into a local vector store, and answers questions by retrieving the most relevant chunks and passing them to a Groq-hosted Llama model — ensuring answers are always grounded in the source material.

---

## 🏗 System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        DATA INGESTION PIPELINE                      │
│                                                                     │
│   data/Medical_book.pdf                                             │
│          │                                                          │
│          ▼                                                          │
│   src/helper.py ──► load_pdf_file()                                 │
│          │          DirectoryLoader + PyPDFLoader                   │
│          │                                                          │
│          ▼                                                          │
│   src/helper.py ──► filter_to_minimal_docs()                        │
│          │          strips metadata to {"source": path}             │
│          │                                                          │
│          ▼                                                          │
│   src/helper.py ──► text_split()                                    │
│          │          chunk_size=500, chunk_overlap=20                │
│          │                                                          │
│          ▼                                                          │
│   src/helper.py ──► download_hugging_face_embeddings()              │
│          │          all-MiniLM-L6-v2  →  384-dim vectors            │
│          │                                                          │
│          ▼                                                          │
│   ChromaDB  (persisted locally at chroma_store/)                    │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              │  similarity search (k=3)
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          INFERENCE PIPELINE                         │
│                                                                     │
│   User Question                                                     │
│          │                                                          │
│          ▼                                                          │
│   ChromaDB Retriever ──► top-3 most relevant chunks                 │
│          │                                                          │
│          ▼                                                          │
│   src/prompt.py ──► system_prompt   ({context} filled at runtime)   │
│          │                                                          │
│          ▼                                                          │
│   create_stuff_documents_chain()  +  create_retrieval_chain()       │
│          │          (LangChain ≥ 1.2 API)                           │
│          │                                                          │
│          ▼                                                          │
│   Groq API ──► llama-3.1-8b-instant   (max_tokens=512)             │
│          │                                                          │
│          ▼                                                          │
│   Grounded Answer  (≤ 3 sentences, context-only)                    │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
End-to-End-Medical-Chatbot/
│
├── 📄 app.py                        # Flask application entry point
├── 📄 store_index.py                # One-time ingestion script (PDF → ChromaDB)
├── 📄 setup.py                      # Package configuration
├── 📄 requirements.txt              # Pinned Python dependencies
│
├── 📂 src/                          # Core business logic (importable package)
│   ├── 🐍 __init__.py
│   ├── 🐍 helper.py                 # load, filter, split, embed utilities
│   └── 🐍 prompt.py                 # system_prompt definition
│
├── 📂 data/                         # PDF knowledge base (gitignored if large)
│   └── 📑 Medical_book.pdf
│
├── 📂 chroma_store/                 # ChromaDB persistence directory (gitignored)
│
├── 📂 templates/
│   └── 🌐 chat.html                 # Flask Jinja2 chat interface
│
├── 📂 static/
│   └── 🎨 style.css                 # Chat UI styles
│
├── 📂 research/
│   └── 📓 demo.ipynb                # Research / exploration notebook
│
├── 📂 all-utils/                    # Auxiliary utilities (logging, pydantic, mem0)
│   ├── 🐍 main.py
│   └── 📄 requirements.txt
│
├── 🐳 Dockerfile                    # Container definition
└── 📓 Medical_Chatbot_Colab.ipynb   # Full end-to-end notebook (no Docker)
```

---

## 🛠 Technology Stack

| Layer | Technology | Version | Cost |
|-------|-----------|---------|------|
| **Language** | Python | ≥ 3.10 | Free |
| **Orchestration** | LangChain | ≥ 1.2.0 | Free |
| **LLM** | Groq · llama-3.1-8b-instant | — | Free tier |
| **Vector Database** | ChromaDB | ≥ 0.5.0 | Free / local |
| **Embeddings** | HuggingFace · all-MiniLM-L6-v2 | 384 dims | Free |
| **PDF Loader** | PyPDF + DirectoryLoader | ≥ 4.0 | Free |
| **Web Framework** | Flask | ≥ 3.1 | Free |
| **Packaging** | setuptools | — | Free |

> **No paid API keys are required** beyond a free Groq account. ChromaDB runs entirely on local disk.

---

## 🔗 LangChain 1.2+ — Import Changes & Compatibility

LangChain 1.2 completed the namespace reorganisation that began in 0.2. All imports in this project follow the **stable, non-deprecated paths**. The table below shows what changed and why:

### Import Migration Reference

| Component | Deprecated (pre-0.2) | Current (≥ 1.2) | File Affected |
|-----------|---------------------|-----------------|---------------|
| `DirectoryLoader` | `from langchain.document_loaders import DirectoryLoader` | `from langchain_community.document_loaders import DirectoryLoader` | `src/helper.py` |
| `PyPDFLoader` | `from langchain.document_loaders import PyPDFLoader` | `from langchain_community.document_loaders import PyPDFLoader` | `src/helper.py` |
| `HuggingFaceEmbeddings` | `from langchain.embeddings import HuggingFaceEmbeddings` | `from langchain_huggingface import HuggingFaceEmbeddings` | `src/helper.py` |
| `RecursiveCharacterTextSplitter` | `from langchain.text_splitter import ...` | `from langchain.text_splitter import ...` *(unchanged)* | `src/helper.py` |
| `Document` schema | `from langchain.schema import Document` | `from langchain_core.documents import Document` | `src/helper.py` |
| `ChatPromptTemplate` | `from langchain.prompts import ChatPromptTemplate` | `from langchain_core.prompts import ChatPromptTemplate` | `app.py` |
| `create_retrieval_chain` | `from langchain.chains import ...` | `from langchain.chains import create_retrieval_chain` *(unchanged)* | `app.py` |
| `create_stuff_documents_chain` | `from langchain.chains.combine_documents import ...` | `from langchain.chains.combine_documents import ...` *(unchanged)* | `app.py` |
| `ChatGroq` | *(not available)* | `from langchain_groq import ChatGroq` | `app.py` |
| `Chroma` vector store | `from langchain.vectorstores import Chroma` | `from langchain_chroma import Chroma` | `store_index.py`, `app.py` |

### Package Installation (LangChain 1.2 Ecosystem)

```bash
pip install \
    langchain>=1.2.0 \
    langchain-community>=0.2.0 \
    langchain-core>=0.2.0 \
    langchain-groq>=0.1.0 \
    langchain-huggingface>=0.0.3 \
    langchain-chroma>=0.1.0
```

> **Why separate packages?**  
> From LangChain 1.0 onward, each integration (HuggingFace, Groq, Chroma, OpenAI, etc.) lives in its own installable sub-package. This prevents transitive dependency bloat — you only install what you use.

---

## 🔄 Swapping the Data Source — What Changes

The project is deliberately structured so that changing the knowledge base source requires touching **only specific, isolated files**. The table below is a complete change guide for every common swap scenario.

---

### Scenario 1 — Different PDF or Additional PDFs

Simply drop new `.pdf` files into the `data/` directory and re-run `store_index.py`. No code changes required.

```bash
cp my_new_medical_reference.pdf data/
python store_index.py
```

The `DirectoryLoader` glob (`*.pdf`) picks up all files automatically.

---

### Scenario 2 — Replace PDF with Plain Text / Markdown / CSV Files

| File | What to Change |
|------|---------------|
| `src/helper.py` | Replace `PyPDFLoader` with the appropriate loader and update `load_pdf_file()` |
| `src/helper.py` | Update the `glob` pattern in `DirectoryLoader` (e.g. `*.txt`, `*.md`, `*.csv`) |
| `store_index.py` | No change required |
| `app.py` | No change required |

**Example — switching to `.txt` files:**

```python
# src/helper.py  (only this function changes)
from langchain_community.document_loaders import TextLoader, DirectoryLoader

def load_pdf_file(data: str) -> List[Document]:
    loader = DirectoryLoader(
        data,
        glob="*.txt",          # <-- change glob pattern
        loader_cls=TextLoader, # <-- change loader class
    )
    return loader.load()
```

---

### Scenario 3 — Replace PDF with a Web URL / Website

| File | What to Change |
|------|---------------|
| `src/helper.py` | Replace `load_pdf_file()` body with `WebBaseLoader` or `RecursiveUrlLoader` |
| `store_index.py` | Pass the URL instead of a directory path |
| `app.py` | No change required |
| `src/prompt.py` | No change required |

```python
# src/helper.py  (only this function changes)
from langchain_community.document_loaders import WebBaseLoader

def load_pdf_file(data: str) -> List[Document]:
    # `data` now holds a URL string
    loader = WebBaseLoader(web_paths=[data])
    return loader.load()
```

```python
# store_index.py  (only the call-site changes)
extracted_data = load_pdf_file(data="https://your-medical-site.com/articles")
```

---

### Scenario 4 — Replace PDF with a SQL / NoSQL Database

| File | What to Change |
|------|---------------|
| `src/helper.py` | Rewrite `load_pdf_file()` to query DB and return `List[Document]` |
| `store_index.py` | Pass DB connection string or config dict instead of a file path |
| `app.py` | No change required |
| `src/prompt.py` | No change required |

```python
# src/helper.py  (only this function changes)
import psycopg2
from langchain_core.documents import Document

def load_pdf_file(data: str) -> List[Document]:
    # `data` is a PostgreSQL DSN: "postgresql://user:pass@host/db"
    conn   = psycopg2.connect(data)
    cursor = conn.cursor()
    cursor.execute("SELECT title, body FROM medical_articles;")
    rows   = cursor.fetchall()
    conn.close()
    return [
        Document(page_content=body, metadata={"source": title})
        for title, body in rows
    ]
```

---

### Scenario 5 — Replace ChromaDB with Pinecone (paid)

If you want to restore the original Pinecone-based vector store, the following files change:

| File | What to Change |
|------|---------------|
| `store_index.py` | Replace `Chroma.from_documents()` with `PineconeVectorStore.from_documents()` |
| `app.py` | Replace `Chroma(...)` with `PineconeVectorStore.from_existing_index(...)` |
| `requirements.txt` | Add `langchain-pinecone`, `pinecone-client`; remove `langchain-chroma`, `chromadb` |
| `.env` / Secrets | Add `PINECONE_API_KEY` and set index region |
| `src/helper.py` | No change required |
| `src/prompt.py` | No change required |

> The `filter_to_minimal_docs()` function in `src/helper.py` was written specifically to handle metadata serialisation quirks that both ChromaDB and Pinecone can encounter. It should be kept regardless of which vector store is used.

---

### Scenario 6 — Replace Groq / Llama with a Different LLM

| File | What to Change |
|------|---------------|
| `app.py` | Swap `ChatGroq(...)` for any `BaseChatModel`-compatible class |
| `.env` / Secrets | Replace `GROQ_API_KEY` with the relevant key |
| `requirements.txt` | Replace `langchain-groq` with the relevant LangChain integration package |
| `src/helper.py` | No change required |
| `src/prompt.py` | Optionally tighten or expand the system prompt |
| `store_index.py` | No change required |

**Supported drop-in replacements (LangChain 1.2):**

```python
# OpenAI GPT-4o
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2)

# Google Gemini
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

# Ollama (fully local, no API key)
from langchain_ollama import ChatOllama
llm = ChatOllama(model="llama3.1:8b", temperature=0.2)
```

---

### Change Impact Summary Matrix

| Change | `src/helper.py` | `src/prompt.py` | `store_index.py` | `app.py` | `requirements.txt` |
|--------|:-:|:-:|:-:|:-:|:-:|
| Different / additional PDF | — | — | — | — | — |
| Different file type (txt, csv, md) | ✏️ loader only | — | — | — | maybe |
| Web URL as source | ✏️ loader only | — | ✏️ path arg | — | maybe |
| SQL / NoSQL database | ✏️ loader only | — | ✏️ conn arg | — | ✏️ |
| ChromaDB → Pinecone | — | — | ✏️ | ✏️ | ✏️ |
| Groq → other LLM | — | optional | — | ✏️ | ✏️ |
| Adjust chunk size / overlap | ✏️ `text_split` | — | re-run | — | — |
| Adjust system prompt | — | ✏️ | — | — | — |

> **Key design insight:** `src/helper.py` is the only file that needs to change when you change the *data source*. `app.py` only changes when you change the *LLM or vector store*. `src/prompt.py` is fully isolated from infrastructure concerns.

---

## ⚙️ Environment Setup

### Prerequisites

- Python 3.10 or higher
- A free [Groq account](https://console.groq.com) (API key, no credit card required)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/End-to-End-Medical-Chatbot.git
cd End-to-End-Medical-Chatbot
```

### 2. Create and Activate a Virtual Environment

```bash
# Using conda (recommended)
conda create -n medibot python=3.10 -y
conda activate medibot

# Or using venv
python -m venv .venv
source .venv/bin/activate    # Linux / macOS
.venv\Scripts\activate       # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```ini
# .env
GROQ_API_KEY="your_groq_api_key_here"
```

> For the notebook workflow, set `GROQ_API_KEY` directly in your runtime environment's secret manager instead of a `.env` file.

---

## 🚀 Running the Pipeline

### Step 1 — Ingest & Index (Run Once)

```bash
python store_index.py
```

This script:
1. Loads all PDFs from `data/`
2. Filters metadata
3. Splits into 500-char chunks
4. Embeds with MiniLM (384 dims)
5. Persists the ChromaDB index to `chroma_store/`

### Step 2 — Launch the Web Application

```bash
python app.py
```

Visit `http://localhost:8080` to interact with the chatbot through the web UI.

### Step 3 — Docker (Optional)

```bash
docker build -t medical-chatbot .
docker run -p 8080:8080 --env-file .env medical-chatbot
```

---

## 📊 Token Limit Strategy

This project is designed to operate comfortably within the **Groq free tier** limits:

| Metric | Groq Free Tier | This Project |
|--------|---------------|-------------|
| Requests / minute | 30 | — |
| Tokens / minute | 6,000 | ~950 per call |
| Tokens / day | 500,000 | — |
| Context window | 128,000 | ~950 used |

**How per-call token usage is kept low:**

```
System prompt        ~  50 tokens
Retrieved context    ~ 375 tokens  (3 chunks × 500 chars × ~0.25 tok/char)
User question        ~  15 tokens
──────────────────────────────────
Input total          ~ 440 tokens

max_tokens (output)    512 tokens
──────────────────────────────────
Total per call       ~ 950 tokens  ✓ well within 6,000 TPM limit
```

To increase output quality at the cost of more tokens, adjust `max_tokens` and `k` in `app.py`:

```python
llm = ChatGroq(model="llama-3.1-8b-instant", max_tokens=1024)  # richer answers
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})    # more context
```

---

## 🔧 Configuration Reference

All tuneable parameters and their locations:

| Parameter | Default | Location | Effect |
|-----------|---------|----------|--------|
| `chunk_size` | `500` | `src/helper.py` → `text_split()` | Larger = more context per chunk, fewer chunks |
| `chunk_overlap` | `20` | `src/helper.py` → `text_split()` | Larger = less mid-sentence cuts |
| `model_name` (embeddings) | `all-MiniLM-L6-v2` | `src/helper.py` → `download_hugging_face_embeddings()` | Change embedding model |
| `system_prompt` | See file | `src/prompt.py` | Controls LLM persona and constraints |
| `k` (retriever) | `3` | `app.py` | Number of chunks retrieved per query |
| `model` (LLM) | `llama-3.1-8b-instant` | `app.py` | LLM model selection |
| `temperature` | `0.2` | `app.py` | Higher = more creative, lower = more factual |
| `max_tokens` | `512` | `app.py` | Max tokens in LLM response |
| `index_name` / collection | `medical_chatbot` | `store_index.py`, `app.py` | Vector store collection name |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome.

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'feat: add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

Please ensure all new code uses **LangChain ≥ 1.2 import paths** as documented in the [LangChain Compatibility section](#-langchain-12--import-changes--compatibility) above.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built with LangChain · Groq · ChromaDB · HuggingFace**

*RAG-powered. Context-grounded. Fully open-source.*

</div>
