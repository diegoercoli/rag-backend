from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ConfidenceLevel


# SQLAlchemy ORM model for ground truth datasets
class GroundTruth(Base):
    __tablename__ = "ground_truth"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    query_id = Column(Integer, ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'), nullable=False)
    hierarchical_metadata_id = Column(Integer,
                                      ForeignKey('retrieval_framework.hierarchical_metadata.id', ondelete='SET NULL'))
    confidence = Column(Enum(ConfidenceLevel, name="confidence_level", schema="retrieval_framework"), nullable=False)

    query = relationship("Query", back_populates="ground_truths")
    hierarchical_metadata = relationship("HierarchicalMetadata")#, back_populates="ground_truths")
