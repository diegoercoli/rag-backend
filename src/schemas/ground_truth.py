from pydantic import BaseModel
from typing import Optional
from src.models import ConfidenceLevel
from src.schemas.hierarchical_metadata import HierarchicalMetadataInput


class GroundTruthBase(BaseModel):
    filename: str
    query_id: int
    hierarchical_metadata_id: Optional[int] = None
    confidence: ConfidenceLevel


class GroundTruthInput(BaseModel):
    """Schema for ground truth input with nested metadata"""
    filename: str
    hierarchical_metadata: Optional[HierarchicalMetadataInput] = None
    confidence: ConfidenceLevel


class GroundTruthCreate(GroundTruthBase):
    pass


class GroundTruthResponse(GroundTruthBase):
    id: int

    class Config:
        from_attributes = True

# ============================================================================
