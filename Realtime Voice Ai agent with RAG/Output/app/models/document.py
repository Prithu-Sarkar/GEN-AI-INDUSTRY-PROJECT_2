from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Document(BaseModel):
    equipment_id: str
    tenant_id: str
    file_name: str
    content_type: str
    size: int
    storage_key: str
    uploaded_by: str
    description: Optional[str] = None
    embedding_status: str = "pending"
    embedding_error: Optional[dict] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {datetime: lambda v: v.isoformat()}
