from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class ExperimentBase(BaseModel):
    start_time: datetime
    configuration_id: int
    dataset_id: int
    vector_db_collection_id: Optional[int] = None

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentUpdate(BaseModel):
    data_ingestion_time: Optional[float] = None
    date_evaluation_time: Optional[float] = None

class ExperimentResponse(ExperimentBase):
    id: int
    data_ingestion_time: Optional[float]
    date_evaluation_time: Optional[float]
    
    class Config:
        from_attributes = True

# ============================================================================
