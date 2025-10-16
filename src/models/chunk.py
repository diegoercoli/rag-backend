# SQLAlchemy ORM model for document chunks
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

class Chunk(Base):
    __tablename__ = "chunk"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    filename = Column(String(255), nullable=False)
    hierarchical_metadata_id = Column(Integer,
                                      ForeignKey('retrieval_framework.hierarchical_metadata.id', ondelete='SET NULL'))

    hierarchical_metadata = relationship("HierarchicalMetadata")#, back_populates="chunks")
    rankings = relationship("Ranking", back_populates="chunk")