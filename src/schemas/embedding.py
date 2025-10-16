from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Pydantic model is
class EmbeddingBase(BaseModel):
    model_name: str = Field(..., title="Name of the embedding model")
    max_input_tokens: int = Field(..., gt=0, description="Maximum number of input tokens the embedding model can handle")

class EmbeddingCreate(EmbeddingBase):
    pass

class EmbeddingUpdate(BaseModel):
    model_name: Optional[str] = Field(None, title="Name of the embedding model")
    max_input_tokens: Optional[int] = Field(None, gt=0, description="Maximum number of input tokens the embedding model can handle")

class EmbeddingResponse(EmbeddingBase):
    id: int
    class Config:
        from_attributes = True



# ============================================================================
