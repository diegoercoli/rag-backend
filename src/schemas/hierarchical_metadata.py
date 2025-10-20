from pydantic import BaseModel
from typing import Optional


class HierarchicalMetadataInput(BaseModel):
    """Schema for hierarchical metadata input"""
    id_section: Optional[str] = None
    section_title: Optional[str] = None
    depth: Optional[int] = None


class HierarchicalMetadataResponse(HierarchicalMetadataInput):
    """Schema for hierarchical metadata response"""
    id: int

    class Config:
        from_attributes = True