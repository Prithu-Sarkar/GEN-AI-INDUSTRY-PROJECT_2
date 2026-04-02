# 🤖 Agentic RAG — PDF Q&A

A conversational PDF question-answering app powered by Groq, FAISS, and Streamlit.

## Stack
- **LLM**: Groq (`llama-3.1-8b-instant`)
- **Embeddings**: HuggingFace (`all-MiniLM-L6-v2`)
- **Vector Store**: FAISS
- **UI**: Streamlit

## How it works
1. Upload a PDF → chunks are embedded and indexed into FAISS
2. Ask a question → top-k relevant chunks are retrieved
3. Chunks + question are sent to Groq LLM → answer is returned

## Setup

```bash
pip install streamlit langchain langchain-groq langchain-community langchain-huggingface faiss-cpu pypdf sentence-transformers
```

Set your Groq API key:
```bash
export GROQ_API_KEY=your_key_here
```

Run the app:
```bash
streamlit run streamlit_app.py
```

## Run on Colab
Use `pyngrok` to tunnel the Streamlit app:
```python
from pyngrok import ngrok
!streamlit run streamlit_app.py &
print(ngrok.connect(8501))
```
