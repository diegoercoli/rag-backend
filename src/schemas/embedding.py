from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EmbeddingBase(BaseModel):
    model_name: str
    max_input_tokens: int

class EmbeddingCreate(EmbeddingBase):
    pass

class EmbeddingResponse(EmbeddingBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
