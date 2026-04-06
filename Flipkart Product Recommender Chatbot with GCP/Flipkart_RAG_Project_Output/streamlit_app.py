# Flipkart AI Assistant — Streamlit UI
# Run with: streamlit run streamlit_app.py
# NOTE: For Colab tunnel use pyngrok (see reference notebook).

import os, time, uuid
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.messages import HumanMessage, SystemMessage
from flipkart.data_converter import DataConverter

GROQ_API_KEY    = os.environ.get("GROQ_API_KEY", "")
LLM_MODEL       = "llama-3.1-8b-instant"
EMBED_MODEL     = "all-MiniLM-L6-v2"

st.set_page_config(page_title="Flipkart AI Chatbot", page_icon="🛒", layout="centered")
st.title("🛒 Flipkart AI Assistant")
st.caption("Powered by Groq · FAISS · HuggingFace Embeddings")

@st.cache_resource(show_spinner="🔍 Building knowledge base ...")
def init_pipeline():
    docs   = DataConverter("data/flipkart_product_review.csv").convert()
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500, chunk_overlap=50
    ).split_documents(docs)
    embed  = HuggingFaceEmbeddings(model_name=EMBED_MODEL)
    vs     = FAISS.from_documents(chunks, embed)
    ret    = vs.as_retriever(search_kwargs={"k": 4})
    llm    = ChatGroq(model=LLM_MODEL, api_key=GROQ_API_KEY, temperature=0)
    return llm, ret, len(chunks)

llm, retriever, n_chunks = init_pipeline()
st.success(f"✅ {n_chunks} review chunks indexed")

if "messages" not in st.session_state:
    st.session_state.messages       = []
    st.session_state.request_count  = 0
    st.session_state.prediction_count = 0

if st.sidebar.button("🔄 New Chat"):
    st.session_state.messages = []
    st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask me about Flipkart products ...")

if user_input:
    st.session_state.request_count += 1
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("🤖 Thinking ..."):
            docs    = retriever.invoke(user_input)
            context = "\n\n".join(
                f"[{i}] Product: {d.metadata.get('product_name','?')}\nReview: {d.page_content}"
                for i, d in enumerate(docs, 1)
            ) or "No relevant reviews found."
            response = llm.invoke([
                SystemMessage(content=(
                    "You are a Flipkart assistant. Answer using ONLY the context below. "
                    "If context is insufficient, say so politely."
                )),
                HumanMessage(content=f"Context:\n{context}\n\nQuestion: {user_input}"),
            ])
            reply = response.content
        st.markdown(reply)
    st.session_state.prediction_count += 1
    st.session_state.messages.append({"role": "assistant", "content": reply})

st.divider()
col1, col2 = st.columns(2)
col1.metric("📥 Requests",    st.session_state.request_count)
col2.metric("🤖 Predictions", st.session_state.prediction_count)
