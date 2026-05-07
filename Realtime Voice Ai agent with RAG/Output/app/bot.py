"""
Core AI bot logic - Groq LLM + RAG tool function call.
In production this is wrapped in a Pipecat WebSocket pipeline.
In Colab we expose run_rag_query() for direct demonstration.
"""
import json
from typing import Dict, Any, List, Optional
from loguru import logger
from groq import AsyncGroq
from app.services.rag import RAGService
from app.config import settings

# System prompt - identical to production bot.py
SYSTEM_PROMPT = """
You are an AI assistant supporting a human call-center agent.

Goal:
Provide the human agent with fast, efficient guidance suitable for real-time conversation.
Speak in natural, concise sentences. Do NOT output JSON.

Behavioral rules:
- Implement a natural, helpful, and professional tone.
- Keep responses brief and to the point (optimized for speech).
- Do not read out chunk IDs or metadata unless explicitly asked.

Knowledge base rules:
- When the customer asks a question or seeks information, call the search_knowledge_base tool.
- Use ONLY facts returned from the knowledge base to answer questions.
- If the knowledge base lacks the answer, briefly suggest that the agent apologize and ask for clarification.
- NEVER invent or guess information.

Content generation:
- Your output will be converted to speech, so avoid special characters or complex formatting.
- Directly address the agent with the guidance or answer.

Answer in one or two sentences and under 30 words.
Answer prices in integers and do not include any decimal places.
"""

# Tool schema - mirrors production FunctionSchema
SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Search the knowledge base for relevant information about equipment",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search query"}
            },
            "required": ["query"],
        },
    },
}

async def run_rag_query(
    user_message: str,
    equipment_id: Optional[str] = None,
    tenant_id: Optional[str] = None,
    conversation_history: Optional[List[Dict]] = None,
) -> Dict[str, Any]:
    """
    Run one turn of the RAG-augmented LLM.
    Mirrors production pipeline: STT output -> LLM -> tool_call -> RAG -> LLM -> TTS input.
    Returns: answer (str), chunks (list), tool_called (bool)
    """
    client = AsyncGroq(api_key=settings.GROQ_API_KEY)
    rag_service = RAGService()

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": user_message})

    retrieved_chunks = []
    tool_called = False

    # First LLM call - may request a tool
    response = await client.chat.completions.create(
        model=settings.GROQ_MODEL,
        messages=messages,
        tools=[SEARCH_TOOL],
        tool_choice="auto",
        max_tokens=512,
        temperature=0.3,
    )

    msg = response.choices[0].message

    if msg.tool_calls:
        tool_called = True
        tool_call = msg.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        query = args.get("query", user_message)
        logger.info(f"Tool called: search_knowledge_base(query={query!r})")
        try:
            result = await rag_service.retrieve(
                query=query, k=5,
                equipment_id=equipment_id,
                tenant_id=tenant_id,
            )
            retrieved_chunks = [
                {"id": m.chunk_id, "text": c.text, "score": c.score, "file": c.file_name}
                for c, m in zip(result.data, result.metadata.chunks)
            ]
            tool_content = json.dumps({"results": [
                {"id": c["id"], "content": c["text"]} for c in retrieved_chunks
            ]})
        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")
            tool_content = json.dumps({"results": []})

        messages.append({
            "role": "assistant", "content": None,
            "tool_calls": [{
                "id": tool_call.id, "type": "function",
                "function": {"name": "search_knowledge_base", "arguments": tool_call.function.arguments},
            }]
        })
        messages.append({"role": "tool", "tool_call_id": tool_call.id, "content": tool_content})

        # Second LLM call - generate final answer grounded in retrieved context
        final_response = await client.chat.completions.create(
            model=settings.GROQ_MODEL,
            messages=messages,
            max_tokens=256,
            temperature=0.3,
        )
        answer = final_response.choices[0].message.content or ""
    else:
        answer = msg.content or ""

    return {"answer": answer.strip(), "chunks": retrieved_chunks, "tool_called": tool_called}
