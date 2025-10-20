from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ComplexityQuery


# SQLAlchemy ORM model for queries
class Query(Base):
    __tablename__ = "query"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    prompt = Column(Text, nullable=False)
    device = Column(String(255))
    customer = Column(String(255))
    obsolete = Column(Boolean, nullable=False, default=False)
    dataset_id = Column(Integer, ForeignKey('retrieval_framework.dataset.id', ondelete='RESTRICT'))
    complexity = Column(Enum(ComplexityQuery, name="complexity_query", schema="retrieval_framework"), nullable=False)
    dataset = relationship("Dataset", back_populates="queries")
    rankings = relationship("Ranking", back_populates="query")
    metrics = relationship("Metrics", back_populates="query")
    ground_truths = relationship("GroundTruth", back_populates="query")