"""
Simple Q&A agent — adapted for Groq/LLaMA.
Course original used Tavily MCP for search.
In Colab we keep it tool-free to avoid npx/Node.js friction.
Add MCPToolset here if TAVILY_API_KEY is available.
"""
import os
from google.adk.agents.llm_agent import LlmAgent

MODEL = os.getenv("ADK_MODEL", "groq/llama-3.3-70b-versatile")

root_agent = LlmAgent(
    model=MODEL,
    name="simple",
    instruction="""
You are a helpful Q&A assistant. Answer factual questions clearly in 3-6 sentences.
Cite your reasoning. If uncertain, say so honestly.
    """.strip(),
    tools=[],  # attach MCPToolset(tavily) here when TAVILY_API_KEY is set
)
