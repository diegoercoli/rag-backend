from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class MetricsBase(BaseModel):
    precision_value: Optional[float] = None
    recall: Optional[float] = None
    f1_score: Optional[float] = None
    ndcg: Optional[float] = None
    mrr: Optional[float] = None
    map_value: Optional[float] = None
    experiment_id: int
    query_id: int

class MetricsCreate(BaseModel):
    experiment_id: int
    query_id: int

class MetricsResponse(MetricsBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
