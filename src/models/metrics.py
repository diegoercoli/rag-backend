from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
# SQLAlchemy ORM model for metric results
class Metrics(Base):
    __tablename__ = "metrics"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    precision_value = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    ndcg = Column(Float)
    mrr = Column(Float)
    map_value = Column(Float)
    experiment_id = Column(Integer, ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'), nullable=False)
    query_id = Column(Integer, ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'), nullable=False)

    experiment = relationship("Experiment", back_populates="metrics")
    query = relationship("Query", back_populates="metrics")
