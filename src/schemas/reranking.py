from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class RerankingBase(BaseModel):
    model_name: str
    max_input_tokens: int


class RerankingCreate(RerankingBase):
    pass


class RerankingResponse(RerankingBase):
    id: int

    class Config:
        from_attributes = True

# ============================================================================
