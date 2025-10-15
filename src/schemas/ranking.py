from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RankingBase(BaseModel):
    rank_position: int
    score: float
    is_relevant: Optional[bool] = None
    chunk_id: int
    query_id: int
    experiment_id: int

class RankingCreate(RankingBase):
    pass

class RankingUpdate(BaseModel):
    is_relevant: Optional[bool] = None

class RankingBulkCreate(BaseModel):
    experiment_id: int
    query_id: int
    results: List[dict]

class RankingResponse(RankingBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
