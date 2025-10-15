# SQLAlchemy ORM model for ranking results
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
class Ranking(Base):
    __tablename__ = "ranking"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    rank_position = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    is_relevant = Column(Boolean)
    chunk_id = Column(Integer, ForeignKey('retrieval_framework.chunk.id', ondelete='CASCADE'), nullable=False)
    query_id = Column(Integer, ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'), nullable=False)

    chunk = relationship("Chunk", back_populates="rankings")
    query = relationship("Query", back_populates="rankings")
    experiment = relationship("Experiment", back_populates="rankings")
