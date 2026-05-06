import os
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Initialise Groq client via LangChain (>=1.2 compatible)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    max_tokens=1024,
    api_key=os.environ["GROQ_API_KEY"]
)

def get_diagnosis(symptoms: list) -> str:
    """
    Given a list of symptom strings, query the LLM for a possible
    diagnosis and suggested cure.

    Args:
        symptoms: List of symptom strings (e.g. [\"fever\", \"cough\"]).

    Returns:
        LLM-generated diagnosis and cure suggestion as a string.
    """
    if not symptoms:
        return "No symptoms detected. Please provide a symptom description."

    prompt = (
        f"Patient has symptoms: {', '.join(symptoms)}. "
        "Suggest possible medical diagnosis and a possible cure for the same. "
        "Be concise and structured."
    )

    messages = [
        SystemMessage(content="You are a helpful medical assistant. Provide structured, clear responses."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)
    return response.content.strip()