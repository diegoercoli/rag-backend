# SQLAlchemy ORM model for query enhancement strategies
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ChunkingType


class QueryEnhancement(Base):
    __tablename__ = "query_enhancement"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    customer = Column(Boolean, nullable=False)
    device_mode = Column(Boolean, nullable=False)

    #configurations = relationship("Configuration", back_populates="query_enhancement")