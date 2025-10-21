from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ExperimentDocumentBase(BaseModel):
    """Base schema for experiment-document association"""
    experiment_id: int
    document_id: int
    hash: Optional[str] = None


class ExperimentDocumentCreate(ExperimentDocumentBase):
    """Schema for creating experiment-document association"""
    pass


class ExperimentDocumentResponse(ExperimentDocumentBase):
    """Schema for experiment-document association response"""
    id: int
    added_at: datetime

    class Config:
        from_attributes = True


class ExperimentDocumentBulkCreate(BaseModel):
    """Schema for bulk creating experiment-document associations"""
    experiment_id: int
    document_ids: list[int]