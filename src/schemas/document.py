from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    filename: str
    version: float
    type: str
    current_hash: str
    knowledge_base_id: Optional[int] = None


class DocumentCreate(DocumentBase):
    pass

class DocumentUpdate(BaseModel):
    knowledge_base_id: Optional[int] = None


class DocumentResponse(DocumentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        use_enum_values = True