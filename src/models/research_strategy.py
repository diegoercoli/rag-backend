from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ResearchType


# SQLAlchemy ORM model for research strategies
class ResearchStrategy(Base):
    __tablename__ = "research_strategy"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    enabled = Column(Boolean, nullable=False)
    pre_retrieval = Column(Integer, nullable=False)
    top_k = Column(Integer, nullable=False)
    rerank_enabled = Column(Integer, nullable=False)
    research_type = Column(Enum(ResearchType, name="research_type", schema="retrieval_framework"), nullable=False)

    alpha = Column(Float, nullable=True)

    #configurations = relationship("Configuration", back_populates="research_strategy")