# holiday_team.py
# The HolidayTeam orchestrates the full agent pipeline.
#
# Execution order:
#   1. Query Validation & Transformation
#   2. Pydantic model validation of the trip request
#   3. Mem0 memory retrieval (personalisation)
#   4. Planner Agent → draft_plan
#   5. Researcher Agent → final_output
#   6. Return AgentState

import sys
import os
import logging

from holiday_management.config.settings import settings
from holiday_management.utils.state import AgentState
from holiday_management.agents.planner import run_planner
from holiday_management.agents.researcher import run_researcher

logger = logging.getLogger(__name__)


class HolidayTeam:
    """
    Orchestrator that coordinates the Planner and Researcher agents.
    Also integrates Mem0 for personalised memory retrieval.
    """

    def __init__(self, enable_memory: bool = True):
        """
        Parameters
        ----------
        enable_memory : If True, retrieve past user preferences via Mem0
                        before planning.  Set False to skip (faster CI runs).
        """
        self.enable_memory = enable_memory
        self._mem = None

        if enable_memory:
            self._init_memory()

    def _init_memory(self):
        """Initialise Mem0 with Groq + ChromaDB."""
        print(f"[DEBUG] Mem0 init: using LLM model {settings.LLM_MODEL} with max_tokens {settings.LLM_MAX_TOKENS}")
        try:
            from mem0 import Memory
            config = {
                "vector_store": {
                    "provider": "chroma",
                    "config": {
                        "collection_name": "holiday_agent_memory",
                        "path": settings.CHROMA_DB_PATH
                    }
                },
                "llm": {
                    "provider": "groq",
                    "config": {
                        "model": settings.LLM_MODEL,
                        "temperature": 0,
                        "max_tokens": settings.LLM_MAX_TOKENS, # Use setting, not hardcoded 512
                        "api_key": os.environ.get("GROQ_API_KEY")
                    }
                },
                "embedder": {
                    "provider": "huggingface",
                    "config": {
                        "model": "all-MiniLM-L6-v2"
                    }
                }
            }
            self._mem = Memory.from_config(config)
            logger.info("Mem0 initialised successfully.")
        except Exception as e:
            logger.warning("Mem0 init failed (%s) — proceeding without memory.", e)
            self._mem = None

    def _get_user_memory(self, user_id: str, query: str) -> str:
        """Retrieve the top-1 relevant memory snippet for this user."""
        if self._mem is None:
            return "No prior preferences recorded."
        try:
            results = self._mem.search(query, filters={"user_id": user_id})
            memories = results.get("results") if isinstance(results, dict) else results
            if memories:
                return memories[0].get("memory", "No preferences.")
        except Exception as e:
            logger.warning("Memory search failed: %s", e)
        return "No prior preferences recorded."

    def run(self,
            request: str,
            destination: str,
            duration_days: int,
            user_id: str = "anonymous") -> AgentState:
        """
        Execute the full planning pipeline.

        Parameters
        ----------
        request       : Raw natural-language trip request.
        destination   : Target destination.
        duration_days : Number of trip days.
        user_id       : Used for Mem0 personalisation.

        Returns
        -------
        AgentState with final_output populated.
        """
        logger.info("[Team] Starting pipeline for: %s (%d days)", destination, duration_days)

        # Initialise shared state
        state = AgentState(request=request, user_id=user_id)

        # Step 1: retrieve user memory for personalisation
        user_memory = self._get_user_memory(user_id, request)
        logger.info("[Team] User memory: %s", user_memory)

        # Step 2: run Planner agent
        logger.info("[Team] Running Planner agent...")
        state = run_planner(state, destination, duration_days, user_memory)
        logger.info("[Team] Draft plan ready (%d chars)", len(state.draft_plan or ""))

        # Step 3: run Researcher agent
        logger.info("[Team] Running Researcher agent...")
        state = run_researcher(state, destination, duration_days)
        logger.info("[Team] Final output ready (%d chars)", len(state.final_output or ""))

        return state


# ── Singleton for direct import (mirrors original project pattern) ──────────
team = HolidayTeam(enable_memory=True)