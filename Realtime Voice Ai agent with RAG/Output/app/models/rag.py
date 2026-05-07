from pydantic import BaseModel, Field
from typing import Optional, List

class ChunkContent(BaseModel):
    text: str = Field(..., description="The actual text content of the chunk")
    file_name: Optional[str] = None
    score: Optional[float] = None

class ChunkMetadata(BaseModel):
    chunk_id: str
    document_id: str
    equipment_id: str
    tenant_id: Optional[str] = None
    chunk_index: int
    score: float
    file_name: str

class RetrievalMetadata(BaseModel):
    query: str
    k: int
    chunks_retrieved: int
    equipment_id: Optional[str] = None
    tenant_id: Optional[str] = None
    chunks: List[ChunkMetadata] = []

class RetrievalResult(BaseModel):
    data: List[ChunkContent]
    metadata: RetrievalMetadata
