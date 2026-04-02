import os, time
import streamlit as st
from typing import List
from pydantic import BaseModel, ConfigDict
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, SystemMessage

# ── constants ────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '')
LLM_MODEL    = 'llama-3.1-8b-instant'
EMBED_MODEL  = 'all-MiniLM-L6-v2'

# ── page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title='Agentic RAG', page_icon='🤖', layout='centered')
st.title('🤖 Agentic RAG — PDF Q&A')
st.caption('Powered by Groq · FAISS · HuggingFace Embeddings')

# ── cached pipeline init ──────────────────────────────────────────────────────
@st.cache_resource
def init_pipeline(pdf_bytes, filename):
    tmp = f'/tmp/{filename}'
    with open(tmp, 'wb') as f:
        f.write(pdf_bytes)
    pages  = PyPDFLoader(tmp).load()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    ).split_documents(pages)
    embed = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs    = FAISS.from_documents(chunks, embed)
    ret   = vs.as_retriever(search_kwargs={'k': 6})
    llm   = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)
    return llm, ret, len(chunks)

# ── RAG answer (no tool-calling API — retriever called directly) ──────────────
def run_rag(question: str, llm, retriever) -> str:
    # Step 1: retrieve relevant chunks directly
    docs = retriever.invoke(question)
    if docs:
        context_parts = []
        for i, d in enumerate(docs, 1):
            page = d.metadata.get('page', '?') if hasattr(d, 'metadata') else '?'
            context_parts.append(f'[{i}] (page={page})\n{d.page_content}')
        context = '\n\n'.join(context_parts)
    else:
        context = 'No relevant passages found in the document.'
    # Step 2: send context + question to LLM — plain chat, no tools
    messages = [
        SystemMessage(content=(
            'You are a helpful RAG assistant. '
            'Answer the question using ONLY the context passages provided below. '
            'If the context does not contain the answer, say so clearly.'
        )),
        HumanMessage(content=f'Context:\n{context}\n\nQuestion: {question}'),
    ]
    response = llm.invoke(messages)
    return response.content

# ── sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header('📄 Upload PDF')
    uploaded_file = st.file_uploader('Choose a PDF', type='pdf')
    st.markdown('---')
    st.caption(f'Model: {LLM_MODEL}')
    st.caption(f'Embeddings: {EMBED_MODEL}')

if not uploaded_file:
    st.info('👈 Upload a PDF from the sidebar to get started.')
    st.stop()

with st.spinner('🔄 Initialising pipeline (first run ~30s) …'):
    llm, retriever, n_chunks = init_pipeline(
        uploaded_file.read(), uploaded_file.name
    )
st.success(f'✅ Ready — {n_chunks} chunks indexed from **{uploaded_file.name}**')

# ── chat history ──────────────────────────────────────────────────────────────
if 'history' not in st.session_state:
    st.session_state.history = []

for turn in st.session_state.history:
    with st.chat_message('user'):
        st.write(turn['q'])
    with st.chat_message('assistant'):
        st.write(turn['a'])
        st.caption(f"⏱️ {turn['t']:.2f}s")

# ── chat input ────────────────────────────────────────────────────────────────
question = st.chat_input('Ask a question about your PDF …')
if question:
    with st.chat_message('user'):
        st.write(question)
    with st.chat_message('assistant'):
        with st.spinner('🤔 Thinking …'):
            t0      = time.time()
            answer  = run_rag(question, llm, retriever)
            elapsed = time.time() - t0
        st.write(answer)
        st.caption(f'⏱️ {elapsed:.2f}s')
    st.session_state.history.append({'q': question, 'a': answer, 't': elapsed})
