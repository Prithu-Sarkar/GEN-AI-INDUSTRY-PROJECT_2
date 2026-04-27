import os
import gradio as gr
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

# ── Config ────────────────────────────────────────────────────
CHROMA_DIR = "./chroma_vectorstore"
COLLECTION_NAME = "air_india_docs"
LLM_PROVIDER = "groq"  # Change to "openai" if needed

# ── Embeddings & Vector Store ─────────────────────────────────
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True},
)
vector_store = Chroma(
    collection_name=COLLECTION_NAME,
    embedding_function=embeddings,
    persist_directory=CHROMA_DIR,
)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# ── LLM ───────────────────────────────────────────────────────
if LLM_PROVIDER == "groq":
    llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0, max_tokens=512)
else:
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0, max_tokens=512)

# ── RAG Chain ─────────────────────────────────────────────────
def format_docs(docs):
    return "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'unknown')}, Page: {doc.metadata.get('page', 'N/A')}]\n{doc.page_content}"
        for doc in docs
    )

prompt = ChatPromptTemplate.from_template("""
You are a helpful Air India assistant.
Use ONLY the context below to answer. If the answer is not in the context,
say: "I don't have enough information to answer that from the provided documents."

Context:
{context}

Question: {question}

Answer:""")

rag_chain = (
    RunnableParallel(context=(retriever | format_docs), question=RunnablePassthrough())
    | prompt | llm | StrOutputParser()
)

# ── Response helper ───────────────────────────────────────────
def get_response(question):
    source_docs = retriever.invoke(question)
    answer = rag_chain.invoke(question)
    sources = list({
        f"{doc.metadata.get('source', 'unknown')} (p.{doc.metadata.get('page', 'N/A')})"
        for doc in source_docs
    })
    return {"answer": answer, "sources": sources}

# ── Gradio UI ─────────────────────────────────────────────────
def chat(user_message, history):
    if not user_message.strip():
        return "", history
    result = get_response(user_message)
    answer = result["answer"]
    if result["sources"]:
        answer += "\n\n📎 **Sources:**\n" + "\n".join(f"• {s}" for s in result["sources"])
    history.append((user_message, answer))
    return "", history

def clear_chat():
    return [], []

with gr.Blocks(title="✈️ Air India RAG Chatbot", theme=gr.themes.Soft(primary_hue="red")) as demo:
    gr.HTML("""
        <div style="text-align:center; padding:20px 0 10px;">
            <h1 style="font-size:2rem; color:#c8102e;">✈️ Air India RAG Chatbot</h1>
            <p style="color:#555;">Ask questions about Air India based on your uploaded documents.</p>
        </div>
    """)
    chatbot = gr.Chatbot(label="Chat", height=480, bubble_full_width=False, show_copy_button=True)
    with gr.Row():
        txt = gr.Textbox(placeholder="Ask something about Air India...", show_label=False, scale=8)
        send_btn = gr.Button("Send ✈️", variant="primary", scale=1)
    clear_btn = gr.Button("🗑️ Clear Chat", variant="secondary")
    gr.Examples(
        examples=[
            ["What are Air India's international routes?"],
            ["Tell me about Air India's history and ownership."],
            ["What domestic routes does Air India operate?"],
        ],
        inputs=txt, label="💡 Sample Questions",
    )
    state = gr.State([])
    txt.submit(chat, [txt, state], [txt, chatbot])
    txt.submit(lambda h: h, [chatbot], [state])
    send_btn.click(chat, [txt, state], [txt, chatbot])
    send_btn.click(lambda h: h, [chatbot], [state])
    clear_btn.click(clear_chat, outputs=[chatbot, state])

if __name__ == "__main__":
    demo.launch()
