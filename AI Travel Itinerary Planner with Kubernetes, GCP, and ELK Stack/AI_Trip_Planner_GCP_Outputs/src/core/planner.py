from langchain_core.messages import HumanMessage, AIMessage
from src.agents.travel_agent import agent
from src.utils.logger import get_logger
from src.utils.custom_exception import CustomException

logger = get_logger(__name__)

class TravelPlanner:
    def __init__(self):
        self.messages = []
        logger.info("TravelPlanner initialized")

    def create_itinerary(
        self,
        city: str,
        days: int,
        interests: list,
        style: str,
        pace: str,
        month: str = None
    ) -> str:
        try:
            user_prompt = f"""
            Plan a {days}-day trip to {city}

            Interests: {', '.join(interests)}
            Travel Style: {style}
            Pace: {pace}
            Month: {month or 'Any'}

            Provide a detailed day-wise itinerary with:
            - Morning, afternoon and evening activities for each day
            - Food and restaurant recommendations
            - Local tips and travel advice
            - Estimated costs where possible
            """.strip()

            self.messages.append(HumanMessage(content=user_prompt))
            response = agent.invoke({"messages": self.messages})

            # Safe extraction: find last AIMessage with content
            final_answer = None
            for message in reversed(response["messages"]):
                if isinstance(message, AIMessage) and message.content:
                    final_answer = message.content
                    break

            if not final_answer:
                final_answer = response["messages"][-1].content

            self.messages.append(AIMessage(content=final_answer))
            logger.info(f"Itinerary generated for {city}")
            return final_answer

        except Exception as e:
            logger.error(f"Planner error: {e}")
            raise CustomException("Failed to generate itinerary", e)