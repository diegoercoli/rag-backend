from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ConfigurationBase(BaseModel):
    idconfiguration: str
    name: str
    embedding_id: Optional[int] = None
    reranking_id: Optional[int] = None
    chunking_id: Optional[int] = None
    query_enhancement_id: Optional[int] = None
    preprocessing_id: Optional[int] = None
    research_strategy_id: Optional[int] = None

class ConfigurationCreate(ConfigurationBase):
    pass

class ConfigurationResponse(ConfigurationBase):
    id: int
    
    class Config:
        from_attributes = True

# ============================================================================
