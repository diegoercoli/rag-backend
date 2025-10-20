# ============================================================================
# src/schemas/query.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from src.models.enums import ComplexityQuery
from src.schemas.ground_truth import GroundTruthResponse



class QueryBase(BaseModel):
    position_id: int = Field(..., ge=1, description="Relative position of query within the dataset (1, 2, 3, ...)")
    version: int = Field(..., ge=1, description="Version number of the query")
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    complexity: ComplexityQuery
    obsolete: bool = Field(default=False)

    class Config:
        from_attributes = True
        use_enum_values = False


class QueryInput(BaseModel):
    """Schema for query input with nested ground truths (for dataset creation)"""
    position_id: int = Field(..., ge=1, description="Relative position of query within the dataset")
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    complexity: ComplexityQuery
    ground_truths: List['GroundTruthInput'] = Field(default_factory=list)

    @validator('complexity', pre=True)
    def validate_complexity(cls, v):
        """Handle complexity enum conversion"""
        if isinstance(v, str):
            try:
                return ComplexityQuery(v)
            except ValueError:
                # Try to match by replacing underscores
                normalized = v.replace('_', '')
                for comp in ComplexityQuery:
                    if comp.value.replace('_', '').lower() == normalized.lower():
                        return comp
                raise ValueError(f"Invalid complexity: {v}")
        return v

    class Config:
        from_attributes = True
        use_enum_values = False


class QueryCreate(BaseModel):
    """Schema for creating a single query"""
    position_id: int = Field(..., ge=1, description="Relative position of query within the dataset")
    version: int = Field(..., ge=1, description="Version number")
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    dataset_id: int
    complexity: ComplexityQuery
    obsolete: bool = Field(default=False)

    class Config:
        from_attributes = True
        use_enum_values = False


class QueryUpdate(BaseModel):
    """Schema for updating a query"""
    prompt: Optional[str] = None
    device: Optional[str] = None
    customer: Optional[str] = None
    complexity: Optional[ComplexityQuery] = None
    obsolete: Optional[bool] = None

    class Config:
        from_attributes = True


class QueryResponse(BaseModel):
    """Schema for query response"""
    id: int  # Auto-increment ID
    position_id: int
    dataset_id: int
    version: int
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    complexity: ComplexityQuery
    obsolete: bool
    created_at: datetime
    ground_truths: List[GroundTruthResponse] = []  # Add this line


    class Config:
        from_attributes = True
        use_enum_values = True  # Convert enums to values in response


# Import for forward reference resolution
from src.schemas.ground_truth import GroundTruthInput, GroundTruthResponse

QueryInput.model_rebuild()