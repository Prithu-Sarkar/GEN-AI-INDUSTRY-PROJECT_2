# Medical Chatbot - Project Summary

## Stack (all free / open-source)
- LLM       : Groq llama-3.1-8b-instant (free tier)
- Vector DB : ChromaDB (local, free, no API key)
- Embeddings: HuggingFace all-MiniLM-L6-v2 (free, 384 dims)
- Framework : LangChain >= 0.2
- PDF Loader: PyPDFLoader (langchain-community)

## Token Limit Compliance (Groq free tier)
- Free limit  : 6,000 tokens/min, 500,000 tokens/day
- Retriever k : 3 chunks x 500 chars = ~375 context tokens
- System prompt: ~50 tokens
- max_tokens  : 512 (capped in ChatGroq init)
- Estimated per-call: ~950 tokens (well within limits)

## Output Files
- phase5_load_summary.txt     : PDF loading summary
- phase5_chunks_summary.txt   : Text chunk details
- phase5_vectorstore_summary.txt : ChromaDB config
- phase6_rag_chain_config.txt : RAG chain parameters
- phase7_qa_demo_output.txt   : Sample Q&A responses
- src_helper.py               : src/helper.py (LangChain >= 0.2)
- src_prompt.py               : src/prompt.py (system prompt)
