from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ResearchStrategyBase(BaseModel):
    enabled: bool
    pre_retrieval: int
    top_k: int
    rerank_enabled: int
    alpha: Optional[float] = None

class ResearchStrategyCreate(ResearchStrategyBase):
    pass

class ResearchStrategyResponse(ResearchStrategyBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
