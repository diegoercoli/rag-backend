from pydantic import BaseModel, validator
from typing import Optional, Union, List
from datetime import datetime
from src.models.enums import ConfidenceLevel
from pydantic import BaseModel
from typing import Optional
from src.models import ConfidenceLevel
from src.schemas.hierarchical_metadata import HierarchicalMetadataInput, HierarchicalMetadataResponse


class GroundTruthBase(BaseModel):
    filename: str
    hierarchical_metadata_id: Optional[int] = None
    confidence: ConfidenceLevel


class GroundTruthInput(BaseModel):
    """Schema for ground truth input with nested metadata"""
    filename: str
    hierarchical_metadata: Optional[HierarchicalMetadataInput] = None
    confidence: ConfidenceLevel


class GroundTruthCreate(BaseModel):
    """Schema for creating ground truth (includes query_id for direct creation)"""
    filename: str
    query_id: int
    hierarchical_metadata_id: Optional[int] = None
    confidence: ConfidenceLevel

    class Config:
        from_attributes = True


class GroundTruthResponse(BaseModel):
    """Schema for ground truth response (excludes query_id since it's N:N)"""
    id: int
    filename: str
    hierarchical_metadata_id: Optional[int] = None
    confidence: str  # Will be "Low", "Medium", or "High"
    hierarchical_metadata: Optional[HierarchicalMetadataResponse] = None  # Add nested metadata


    class Config:
        from_attributes = True
        use_enum_values = True


# ============================================================================