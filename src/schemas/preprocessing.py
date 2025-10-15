from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PreprocessingBase(BaseModel):
    lowercase: bool

class PreprocessingCreate(PreprocessingBase):
    pass

class PreprocessingResponse(PreprocessingBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
