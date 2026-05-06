import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Groq LLM for summarisation (llama-instant is fast; versatile for quality)
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=512,
    api_key=os.environ["GROQ_API_KEY"]
)

def summarize_text(text: str) -> str:
    """
    Summarise medical PubMed abstract text using Groq LLM.

    Args:
        text: Raw abstract text (concatenated from multiple articles).

    Returns:
        Concise summary string.
    """
    if not text or not text.strip():
        return "No abstract text provided to summarise."

    prompt = f"""Summarize the following medical research abstract in a clear, concise paragraph:

{text}"""

    messages = [
        SystemMessage(content="You are a medical research summarizer. Provide accurate, concise summaries."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content.strip()