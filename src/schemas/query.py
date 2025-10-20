from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from src.models import ComplexityQuery


class QueryBase(BaseModel):
    prompt: str
    device: Optional[str] = None
    customer: Optional[str] = None
    dataset_id: Optional[int] = None
    complexity: ComplexityQuery
    obsolete: bool = Field(default=False)  # Explicit default with Field



class QueryCreate(QueryBase):
    pass


class QueryUpdate(BaseModel):
    obsolete: Optional[bool] = None


class QueryResponse(QueryBase):
    id: int

    class Config:
        from_attributes = True
# ============================================================================
