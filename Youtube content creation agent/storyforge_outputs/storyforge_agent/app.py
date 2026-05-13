
import os
import sys
from typing import Optional

# LangChain ≥ 1.2 imports (new-style: langchain-groq, langchain-core)
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient

# ── Model configuration ─────────────────────────────────────────────
# llama-3.1-8b-instant  : low latency, generous free-tier token allowance
# llama-3.3-70b-versatile: higher quality, used when deep reasoning is needed
MODEL_INSTANT    = "llama-3.1-8b-instant"
MODEL_VERSATILE  = "llama-3.3-70b-versatile"

# Token budgets chosen conservatively to stay within Groq free-tier limits.
MAX_TOKENS_SUMMARY = 512   # ~400 words output
MAX_TOKENS_SCRIPT  = 300   # ~120-word video script


def _get_llm(model: str, max_tokens: int) -> ChatGroq:
    """Initialise a ChatGroq LLM with the given model and token ceiling."""
    return ChatGroq(
        model=model,
        temperature=0.7,
        max_tokens=max_tokens,
        api_key=os.environ.get("GROQ_API_KEY"),
    )


def _get_tavily() -> TavilyClient:
    """Return a configured Tavily search client."""
    return TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))


# ── Phase 1: Real-time web research ────────────────────────────────
def get_realtime_info(query: str) -> Optional[str]:
    """
    Search the web with Tavily, then summarise results using LLaMA-instant.
    Returns a ~200-word human-readable summary or None on failure.
    """
    tavily = _get_tavily()

    try:
        resp = tavily.search(query=query, max_results=3, topic="general")
    except Exception as exc:
        print(f"[Tavily] search error: {exc}", file=sys.stderr)
        return None

    # Build a compact context string from search snippets.
    if resp and resp.get("results"):
        parts = []

        for r in resp["results"]:
            title = r.get("title", "")
            snippet = r.get("snippet") or r.get("content", "")[:300]
            url = r.get("url", "")

            parts.append(
                f"Title: {title}"
                f"\nSnippet: {snippet}"
                f"\nURL: {url}"
            )

        source_info = "\n---\n".join(parts)

    else:
        source_info = f"No recent results found for '{query}'."

    # LangChain prompt → LLM → string output parser
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content=(
                "You are a professional researcher. Write an accurate, engaging, "
                "human-like summary (~200 words) from the provided search results. "
                "Be factual and highlight key takeaways. No greetings."
            )
        ),
        HumanMessage(
            content=(
                f"Topic: {query}\n\n"
                f"Search results:\n{source_info}\n\n"
                "Write the summary now."
            )
        ),
    ])

    chain = prompt | _get_llm(MODEL_INSTANT, MAX_TOKENS_SUMMARY) | StrOutputParser()

    try:
        return chain.invoke({})
    except Exception as exc:
        print(f"[LLM] summary error: {exc}", file=sys.stderr)
        return source_info   # graceful fallback to raw snippets


# ── Phase 2: Video-script generation ───────────────────────────────
def generate_video_script(info_text: str) -> Optional[str]:
    """
    Convert a research summary into a short YouTube / Reels script (~100-120 words).
    Uses llama-3.3-70b-versatile for higher creative quality.
    """
    prompt = ChatPromptTemplate.from_messages([
        SystemMessage(
            content=(
                "You are a creative scriptwriter for YouTube Shorts and Instagram Reels. "
                "Write an engaging script with a strong hook and a clear call-to-action. "
                "Keep it to 100-120 words maximum."
            )
        ),
        HumanMessage(
            content=f"Research summary:\n{info_text}\n\nWrite the video script now."
        ),
    ])

    chain = prompt | _get_llm(MODEL_VERSATILE, MAX_TOKENS_SCRIPT) | StrOutputParser()

    try:
        return chain.invoke({})
    except Exception as exc:
        print(f"[LLM] script error: {exc}", file=sys.stderr)
        return None
