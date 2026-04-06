from typing import List, Optional
from langchain_core.documents import Document
from langchain_core.messages import (
    HumanMessage, SystemMessage, ToolMessage, AIMessage
)
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, ConfigDict
from flipkart.config import Config


# ── Typed state ───────────────────────────────────────────────────────────
class RAGState(BaseModel):
    question      : str
    retrieved_docs: List[Document] = []
    answer        : str = ""
    model_config = ConfigDict(arbitrary_types_allowed=True)


# ── Tool factory ──────────────────────────────────────────────────────────
def _make_retriever_tool(retriever):

    @tool
    def search_flipkart_reviews(query: str) -> str:
        """
        Search Flipkart product reviews for information relevant to the query.
        Always call this tool first before answering any product question.
        """
        docs: List[Document] = retriever.invoke(query)
        if not docs:
            return "No relevant product reviews found."
        parts = []
        for i, d in enumerate(docs, 1):
            product = d.metadata.get("product_name", "Unknown product")
            parts.append(f"[{i}] Product: {product}\nReview: {d.page_content}")
        return "\n\n".join(parts)

    return search_flipkart_reviews


# ── RAGNodes ──────────────────────────────────────────────────────────────
class RAGNodes:
    """Node functions for the LangGraph RAG workflow (Groq-safe tool loop)."""

    SYSTEM_PROMPT = (
        "You are a Flipkart e-commerce assistant. "
        "Always use search_flipkart_reviews to look up relevant product reviews "
        "before answering. Summarise findings clearly and helpfully. "
        "If you cannot find an answer say: "
        "'I don't have enough information on that. Please contact customer care.'"
    )

    def __init__(self, retriever, llm, max_iterations: int = 5):
        self.retriever       = retriever
        self.llm             = llm
        self.max_iterations  = max_iterations
        self._tool           = _make_retriever_tool(retriever)
        self._tool_map       = {self._tool.name: self._tool}
        self._llm_with_tools = llm.bind_tools([self._tool])

    def retrieve_docs(self, state: RAGState) -> RAGState:
        """Pre-fetch top-k docs so state.retrieved_docs is always populated."""
        docs = self.retriever.invoke(state.question)
        return RAGState(question=state.question, retrieved_docs=docs)

    def generate_answer(self, state: RAGState) -> RAGState:
        """
        Groq-compatible agentic tool loop.
        Uses bind_tools + manual ToolMessage loop (avoids Groq BadRequestError).
        """
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=state.question),
        ]
        response: Optional[AIMessage] = None

        for _ in range(self.max_iterations):
            response = self._llm_with_tools.invoke(messages)
            messages.append(response)

            if not getattr(response, "tool_calls", None):
                break  # LLM produced a final answer

            for tc in response.tool_calls:
                name = tc["name"]
                args = tc["args"]
                tid  = tc["id"]
                try:
                    result = self._tool_map[name].invoke(args) if name in self._tool_map else f"Unknown tool: {name}"
                except Exception as e:
                    result = f"Tool error: {e}"
                messages.append(ToolMessage(content=str(result), tool_call_id=tid))
        else:
            response = self._llm_with_tools.invoke(
                messages + [HumanMessage(content="Please provide your final answer now.")]
            )

        answer = response.content if response else "Could not generate an answer."
        return RAGState(
            question=state.question,
            retrieved_docs=state.retrieved_docs,
            answer=answer,
        )


# ── GraphBuilder ──────────────────────────────────────────────────────────
class GraphBuilder:
    """Assembles and compiles the LangGraph RAG workflow."""

    def __init__(self, retriever, llm):
        self.nodes = RAGNodes(retriever, llm)
        self.graph = None

    def build(self):
        builder = StateGraph(RAGState)
        builder.add_node("retriever", self.nodes.retrieve_docs)
        builder.add_node("responder", self.nodes.generate_answer)
        builder.set_entry_point("retriever")
        builder.add_edge("retriever", "responder")
        builder.add_edge("responder", END)
        self.graph = builder.compile()
        print("✅ LangGraph compiled → retriever ➜ responder ➜ END")
        return self.graph

    def run(self, question: str) -> dict:
        if self.graph is None:
            self.build()
        return self.graph.invoke(RAGState(question=question))
