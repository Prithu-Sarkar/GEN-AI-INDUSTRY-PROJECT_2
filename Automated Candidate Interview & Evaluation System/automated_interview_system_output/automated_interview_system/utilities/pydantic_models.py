from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional, List

class SearchRequest(BaseModel):
    user_id: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    query: str = Field(..., min_length=1, max_length=200)
    tags: Optional[List[str]] = Field(default_factory=list)

    @field_validator("query")
    def query_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Query must not be empty or whitespace")
        return value.strip()


class SearchResponse(BaseModel):
    status: str
    message: str
    result_count: int = Field(0, ge=0)
    results: List[dict] = Field(default_factory=list)
    processed_at: datetime = Field(default_factory=datetime.utcnow)


def build_search_response(request: SearchRequest) -> SearchResponse:
    example_results = [{"id": 1, "title": "Example item", "query": request.query}]
    return SearchResponse(
        status="success",
        message=f"Search completed for user {request.user_id}",
        result_count=len(example_results),
        results=example_results,
    )


def demo() -> None:
    payload = {
        "user_id": "user123",
        "email": "user@example.com",
        "query": "search for utilities",
        "tags": ["example", "demo"],
    }
    req = SearchRequest(**payload)
    resp = build_search_response(req)
    print("Request:", req.model_dump_json(indent=2))
    print("Response:", resp.model_dump_json(indent=2))