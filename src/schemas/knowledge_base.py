from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class KnowledgeBaseCreate(BaseModel):
    document_id: int
    experiment_id: int

class KnowledgeBaseBulkCreate(BaseModel):
    experiment_id: int
    document_ids: List[int]

class KnowledgeBaseResponse(BaseModel):
    id: int
    document_id: int
    experiment_id: int
    added_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
