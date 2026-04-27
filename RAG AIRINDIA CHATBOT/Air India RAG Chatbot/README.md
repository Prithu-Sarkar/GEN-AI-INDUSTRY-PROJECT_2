# ✈️ Air India RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about Air India using uploaded PDF documents. Built with LangChain, ChromaDB, and Groq/OpenAI, with an interactive Gradio interface.

---

## 🧠 Tech Stack

| Layer | Technology |
|---|---|
| Framework | LangChain 0.2+ (LCEL) |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| LLM | Groq (`llama-3.1-8b-instant`) / OpenAI (`gpt-3.5-turbo`) |
| UI | Gradio |
| PDF Parsing | PyPDF |

---

## 📁 Project Structure

```
air-india-rag-chatbot/
├── Air_India_RAG_Chatbot.ipynb   # Main notebook (ingestion + RAG chain + UI)
├── app.py                        # Standalone Gradio app for local deployment
├── chroma_vectorstore/           # Persisted vector store (auto-generated)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A [Groq API key](https://console.groq.com/) (free) or OpenAI API key

### Installation

```bash
pip install langchain==0.2.16 langchain-community==0.2.16 langchain-chroma==0.1.4 \
            langchain-groq==0.1.9 langchain-openai==0.1.23 langchain-huggingface==0.0.3 \
            chromadb==0.5.3 sentence-transformers==3.0.1 pypdf==4.3.1 gradio==4.42.0
```

### Environment Variables

```bash
export GROQ_API_KEY=your_groq_api_key_here
# Optional — only if using OpenAI
export OPENAI_API_KEY=your_openai_api_key_here
```

---

## 📓 Running the Notebook

1. Open `Air_India_RAG_Chatbot.ipynb` in Jupyter or any compatible environment
2. Add your API keys to the secrets/environment
3. Upload your Air India PDF documents when prompted
4. Run all cells sequentially
5. The Gradio UI launches at the end with a shareable link

---

## 🖥️ Running the App Locally

Ensure the `chroma_vectorstore/` directory exists (generated after running the notebook at least once), then:

```bash
python app.py
```

The app will be available at `http://localhost:7860`

> To switch LLM provider, change `LLM_PROVIDER = "groq"` to `"openai"` inside `app.py`.

---

## ⚙️ How It Works

```
PDF Documents
     │
     ▼
PyPDF Loader → Text Splitter (chunk_size=1000, overlap=200)
     │
     ▼
HuggingFace Embeddings → ChromaDB Vector Store
     │
     ▼
User Query → Similarity Search (top-4 chunks)
     │
     ▼
RAG Prompt + Retrieved Context → Groq / OpenAI LLM
     │
     ▼
Answer + Source Citations
```

---

## 💬 Sample Questions

- *What are Air India's international routes?*
- *Tell me about Air India's history and ownership.*
- *What domestic routes does Air India operate?*
- *What major accidents has Air India had?*
- *What are the employee service regulations?*

---

## 🔑 API Keys

| Provider | Where to get it | Required |
|---|---|---|
| Groq | [console.groq.com](https://console.groq.com/) | Yes (default) |
| OpenAI | [platform.openai.com](https://platform.openai.com/) | Only if switching provider |

---

## 📄 License

This project is intended for educational and research purposes.
