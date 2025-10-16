from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ChunkingType


class Chunking(Base):
    __tablename__ = "chunking"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    num_tokens = Column(Integer, nullable=False)
    type = Column(Enum(ChunkingType, name="chunking_type", schema="retrieval_framework"), nullable=False)

    #configurations = relationship("Configuration", back_populates="chunking")