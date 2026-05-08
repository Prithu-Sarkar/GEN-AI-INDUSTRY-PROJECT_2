# state.py
# Defines the shared State dataclass that travels through every agent.
#
# Agent flow:
#   User Query ─→ [State.request] ─→ Planner ─→ [State.draft_plan]
#              ─→ Researcher ─→ [State.research_data]
#              ─→ final_output string

from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class AgentState:
    """
    Central state object passed between every agent in the pipeline.

    Attributes
    ----------
    request        : Raw natural-language trip request from the user.
    user_id        : Identifier used for Mem0 personalisation lookup.
    draft_plan     : Skeleton itinerary produced by the Planner agent.
    research_data  : Verified facts dict produced by the Researcher agent.
    final_output   : Formatted Markdown travel guide (final deliverable).
    metadata       : Arbitrary metadata bag (token counts, timings, etc.).
    """

    request:       str
    user_id:       str = "anonymous"
    draft_plan:    Optional[str] = None
    research_data: Dict[str, Any] = field(default_factory=dict)
    final_output:  Optional[str] = None
    messages:      List[Dict[str, str]] = field(default_factory=list)
    metadata:      Dict[str, Any] = field(default_factory=dict)

    def add_message(self, role: str, content: str) -> None:
        """Append a message to the conversation history."""
        self.messages.append({"role": role, "content": content})

    def is_complete(self) -> bool:
        """True when the pipeline has produced a final itinerary."""
        return self.final_output is not None