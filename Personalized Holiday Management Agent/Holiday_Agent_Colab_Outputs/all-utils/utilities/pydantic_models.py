# pydantic_models.py
# Defines the validated input/output schemas for the Holiday Management Agent.
# Every request flowing into the system is checked against SearchRequest.
# Every response returned is wrapped in SearchResponse.

from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List


# ── Input Schema ──────────────────────────────────────────────────────────────
class SearchRequest(BaseModel):
    """Validated request model for any user search/query coming into the system."""

    user_id: str = Field(..., min_length=3, max_length=50,
                         description="Unique identifier for the user.")
    email: EmailStr  # pydantic automatically validates email format
    query: str = Field(..., min_length=1, max_length=200,
                       description="The user's natural language query.")
    tags: Optional[List[str]] = Field(default_factory=list,
                                      description="Optional topic tags.")

    @field_validator('query')
    def query_must_not_be_empty(cls, value: str) -> str:
        """Strip whitespace and reject blank queries early."""
        if not value.strip():
            raise ValueError('Query must not be empty or whitespace')
        return value.strip()


# ── Output Schema ─────────────────────────────────────────────────────────────
class SearchResponse(BaseModel):
    """Validated response model returned after processing a user query."""

    status: str
    message: str
    result_count: int = Field(0, ge=0,
                              description="Number of results returned (>= 0).")
    results: List[dict] = Field(default_factory=list)
    processed_at: datetime = Field(default_factory=datetime.utcnow,
                                   description="UTC timestamp of processing.")


# ── Holiday-specific Trip Request ─────────────────────────────────────────────
class TripPlanRequest(BaseModel):
    """Schema for a holiday planning request sent to the agent team."""

    user_id: str = Field(..., min_length=3)
    destination: str = Field(..., min_length=2,
                             description="Target travel destination.")
    duration_days: int = Field(..., ge=1, le=30,
                               description="Number of days for the trip.")
    interests: Optional[List[str]] = Field(default_factory=list,
                                           description="User interests, e.g. food, culture.")
    budget: Optional[str] = Field(None,
                                  description="Budget level: low / medium / high.")

    @field_validator('budget')
    def budget_must_be_valid(cls, v):
        if v and v.lower() not in {"low", "medium", "high"}:
            raise ValueError("budget must be 'low', 'medium', or 'high'")
        return v.lower() if v else v


# ── Helper ────────────────────────────────────────────────────────────────────
def build_search_response(request: SearchRequest) -> SearchResponse:
    """Simulates building a search response for a validated request."""
    example_results = [
        {"id": 1, "title": "Example item", "query": request.query},
    ]
    return SearchResponse(
        status="success",
        message=f"Search completed for user {request.user_id}",
        result_count=len(example_results),
        results=example_results,
    )


def demo() -> None:
    """Run a quick validation demo."""
    request_payload = {
        "user_id": "user123",
        "email": "user@example.com",
        "query": "plan a 5-day trip to Paris",
        "tags": ["travel", "europe"],
    }
    request = SearchRequest(**request_payload)
    response = build_search_response(request)

    print("Request model:")
    print(request.model_dump_json(indent=2))
    print()
    print("Response model:")
    print(response.model_dump_json(indent=2))

    # Also test the TripPlanRequest
    trip = TripPlanRequest(
        user_id="user123",
        destination="Tokyo",
        duration_days=7,
        interests=["anime", "food", "temples"],
        budget="medium"
    )
    print()
    print("Trip Plan Request:")
    print(trip.model_dump_json(indent=2))