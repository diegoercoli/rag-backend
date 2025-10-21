from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DocumentBase(BaseModel):
    filename: str
    version: float
    type: str
    hash: str
    knowledge_base_id: Optional[int] = None
    obsolete: bool = Field(default=False)
    deleted: bool = Field(default=False)


class DocumentInput(BaseModel):
    """Schema for document input (no IDs, no dates, no obsolete/deleted flags)"""
    filename: str
    type: str
    hash: str  # Note: 'hash' in input, 'current_hash' in model


class DocumentCreate(DocumentBase):
    pass


class DocumentUpdate(BaseModel):
    knowledge_base_id: Optional[int] = None
    obsolete: Optional[bool] = None
    deleted: Optional[bool] = None


class DocumentResponse(BaseModel):
    """Schema for document response - uses actual database column names"""
    id: int
    filename: str
    version: float
    type: str
    hash: str
    knowledge_base_id: Optional[int] = None
    obsolete: bool
    deleted: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        use_enum_values = True