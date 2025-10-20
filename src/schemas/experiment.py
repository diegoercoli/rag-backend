from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from src.models import ExperimentStatus


class ExperimentBase(BaseModel):
    start_time: datetime
    configuration_id: int
    dataset_id: int
    vector_db_collection_id: Optional[int] = None


class ExperimentCreate(ExperimentBase):
    status: ExperimentStatus = ExperimentStatus.NOT_STARTED


class ExperimentUpdate(BaseModel):
    data_ingestion_time: Optional[float] = None
    date_evaluation_time: Optional[float] = None
    end_time: Optional[datetime] = None
    status: Optional[ExperimentStatus] = None
    error_message: Optional[str] = None


class ExperimentResponse(ExperimentBase):
    id: int
    data_ingestion_time: Optional[float]
    date_evaluation_time: Optional[float]
    end_time: Optional[datetime]
    status: ExperimentStatus
    error_message: Optional[str]

    class Config:
        from_attributes = True
        use_enum_values = True