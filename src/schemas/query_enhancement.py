from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class QueryEnhancementBase(BaseModel):
    customer: bool
    device_mode: bool

class QueryEnhancementCreate(QueryEnhancementBase):
    pass

class QueryEnhancementResponse(QueryEnhancementBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
