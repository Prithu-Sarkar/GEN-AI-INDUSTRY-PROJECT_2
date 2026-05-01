"""
Capital Agent — minimal ADK agent (adapted for Groq/LLaMA).
Original: gemini-2.0-flash  |  Adapted: groq/llama-3.1-8b-instant
"""
import os
from google.adk.agents.llm_agent import LlmAgent

MODEL = os.getenv("ADK_MODEL", "groq/llama-3.1-8b-instant")

root_agent = LlmAgent(
    model=MODEL,
    name="capital_agent",
    instruction=(
        "You answer concisely. If asked for a country's capital, reply with just the capital name "
        "and a short confirmation (one sentence). For other questions, answer helpfully in 2-4 sentences."
    ),
)
