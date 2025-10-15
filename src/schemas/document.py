from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    filename: str
    version: float
    type: str
    hash: str

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
