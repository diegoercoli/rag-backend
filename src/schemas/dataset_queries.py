from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from src.models import ComplexityQuery, ConfidenceLevel


class HierarchicalMetadataInput(BaseModel):
    """Schema for hierarchical metadata input"""
    id_section: Optional[str] = None
    section_title: Optional[str] = None
    depth: Optional[int] = None
    subsection_title: Optional[str] = None


class GroundTruthInput(BaseModel):
    """Schema for ground truth input"""
    filename: str
    hierarchical_metadata: Optional[HierarchicalMetadataInput] = None
    confidence: ConfidenceLevel


class QueryInput(BaseModel):
    """Schema for query input"""
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    complexity: ComplexityQuery
    obsolete: bool = Field(default=False)
    ground_truths: List[GroundTruthInput] = Field(default_factory=list)


class DatasetInput(BaseModel):
    """Schema for dataset input"""
    dataset_name: str



class DatasetBulkCreate(BaseModel):
    """Schema for bulk dataset creation with queries and ground truths"""
    dataset: DatasetInput
    queries: List[QueryInput] = Field(default_factory=list)


class DatasetBulkResponse(BaseModel):
    """Response schema for bulk dataset creation"""
    dataset_id: int
    dataset_name: str
    data_creation: Optional[date] = None
    data_update: Optional[date] = None
    queries_added: int
    queries_updated: int
    queries_marked_obsolete: int
    ground_truths_added: int

    class Config:
        from_attributes = True