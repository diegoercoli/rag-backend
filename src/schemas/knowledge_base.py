from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class KnowledgeBaseBase(BaseModel):
    name: str


class KnowledgeBaseInput(BaseModel):
    """Schema for knowledge base input from external sources"""
    name: str


class KnowledgeBaseCreate(KnowledgeBaseInput):
    """Schema for creating a knowledge base via API with nested documents"""
    documents: List['DocumentInput'] = Field(default_factory=list)


class KnowledgeBaseUpdate(BaseModel):
    name: Optional[str] = None


class KnowledgeBaseResponse(KnowledgeBaseBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class KnowledgeBaseCreateResponse(KnowledgeBaseResponse):
    """Extended response with operation statistics when documents are included"""
    documents_added: int = 0
    documents_updated: int = 0
    documents_marked_obsolete: int = 0
    documents_marked_deleted: int = 0


class KnowledgeBaseWithDocumentsResponse(KnowledgeBaseResponse):
    """Knowledge base response with nested documents"""
    documents: List['DocumentResponse'] = Field(default_factory=list)


# Import for forward reference resolution
from src.schemas.document import DocumentInput, DocumentResponse
KnowledgeBaseCreate.model_rebuild()
KnowledgeBaseWithDocumentsResponse.model_rebuild()