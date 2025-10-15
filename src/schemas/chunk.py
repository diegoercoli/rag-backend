from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ChunkBase(BaseModel):
    text: str
    filename: str
    hierarchical_metadata_id: Optional[int] = None

class ChunkCreate(ChunkBase):
    pass

class ChunkResponse(ChunkBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
