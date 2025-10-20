from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class KnowledgeBaseBase(BaseModel):
    name: str


class KnowledgeBaseCreate(KnowledgeBaseBase):
    pass


class KnowledgeBaseUpdate(BaseModel):
    name: Optional[str] = None


class KnowledgeBaseResponse(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True