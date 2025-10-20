from pydantic import BaseModel, validator
from typing import Optional, Union, List
from datetime import datetime
from src.models.enums import ConfidenceLevel


class GroundTruthBase(BaseModel):
    filename: str
    query_id: int
    hierarchical_metadata_id: Optional[int] = None
    confidence: Union[ConfidenceLevel, str]

    @validator('confidence', pre=True)
    def validate_confidence(cls, v):
        """Convert string to ConfidenceLevel enum"""
        if isinstance(v, str):
            try:
                return ConfidenceLevel(v)
            except ValueError:
                # Try with different casing
                for level in ConfidenceLevel:
                    if level.value.lower() == v.lower():
                        return level
                raise ValueError(f"Invalid confidence level: {v}")
        return v


class GroundTruthInput(BaseModel):
    """Schema for ground truth input with nested metadata"""
    filename: str
    hierarchical_metadata: Optional['HierarchicalMetadataInput'] = None
    confidence: Union[ConfidenceLevel, str]

    @validator('confidence', pre=True)
    def validate_confidence(cls, v):
        """Convert string to ConfidenceLevel enum"""
        if isinstance(v, str):
            try:
                return ConfidenceLevel(v)
            except ValueError:
                # Try with different casing
                for level in ConfidenceLevel:
                    if level.value.lower() == v.lower():
                        return level
                raise ValueError(f"Invalid confidence level: {v}")
        return v

    class Config:
        from_attributes = True
        use_enum_values = False  # Keep enums as enums


class GroundTruthCreate(GroundTruthBase):
    class Config:
        from_attributes = True


class GroundTruthResponse(BaseModel):
    """Complete ground truth response with all fields"""
    id: int
    filename: str
    query_id: int
    hierarchical_metadata_id: Optional[int] = None
    confidence: str  # Will be the string value like "Low", "Medium", "High"

    # Optional: include nested hierarchical metadata if needed
    # hierarchical_metadata: Optional['HierarchicalMetadataResponse'] = None

    class Config:
        from_attributes = True
        use_enum_values = True  # Convert enums to values in response


# ============================================================================
# Import for forward reference resolution
from src.schemas.hierarchical_metadata import HierarchicalMetadataInput

GroundTruthInput.model_rebuild()

# If you want to include nested hierarchical_metadata in the response, uncomment:
# from src.schemas.hierarchical_metadata import HierarchicalMetadataResponse
# GroundTruthResponse.model_rebuild()