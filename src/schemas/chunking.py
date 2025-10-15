from pydantic import BaseModel
from src.models import ChunkingType

class ChunkingBase(BaseModel):
    num_tokens: int
    type: ChunkingType

class ChunkingCreate(ChunkingBase):
    pass

class ChunkingResponse(ChunkingBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
