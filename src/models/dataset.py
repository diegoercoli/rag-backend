from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

# SQLAlchemy ORM model for datasets
class Dataset(Base):
    __tablename__ = "dataset"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    dataset_name = Column(String(100), unique=True, nullable=False)
    data_creation = Column(Date, nullable=False)
    data_update = Column(Date, nullable=True)

    experiments = relationship("Experiment", back_populates="dataset")
    queries = relationship("Query", back_populates="dataset")
