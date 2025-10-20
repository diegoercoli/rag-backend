from datetime import date
from pydantic import BaseModel, Field
from typing import Optional, List


class DatasetBase(BaseModel):
    """Base schema for dataset"""
    dataset_name: str
    data_creation: date
    data_update: Optional[date] = None


class DatasetInput(BaseModel):
    """
    Schema for dataset input from external sources.
    Backend automatically sets data_creation and data_update.
    """
    dataset_name: str


class DatasetCreate(DatasetInput):
    """
    Schema for creating a dataset via API.
    Optionally include nested queries with ground truths.
    """
    queries: List['QueryInput'] = Field(default_factory=list)


class DatasetUpdate(BaseModel):
    """Schema for updating dataset"""
    data_update: Optional[date] = None


class DatasetResponse(DatasetBase):
    """Basic dataset response"""
    id: int

    class Config:
        from_attributes = True


class DatasetCreateResponse(DatasetResponse):
    """Extended response with operation statistics when queries are included"""
    queries_added: int = 0
    queries_updated: int = 0
    queries_marked_obsolete: int = 0
    ground_truths_added: int = 0


# Import for forward reference resolution
from src.schemas.query import QueryInput
DatasetCreate.model_rebuild()

# ============================================================================