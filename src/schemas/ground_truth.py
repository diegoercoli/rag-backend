from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from src.models import ConfidenceLevel


class GroundTruthBase(BaseModel):
    filename: str
    query_id: int
    hierarchical_metadata_id: Optional[int] = None
    confidence: ConfidenceLevel

class GroundTruthCreate(GroundTruthBase):
    pass

class GroundTruthResponse(GroundTruthBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
