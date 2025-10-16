from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

class HierarchicalMetadata(Base):
    __tablename__ = "hierarchical_metadata"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    id_section = Column(String(255))
    section_title = Column(Text)
    depth = Column(Integer)
    subsection_title = Column(Text)

    #chunks = relationship("Chunk", back_populates="hierarchical_metadata")
    #ground_truths = relationship("GroundTruth", back_populates="hierarchical_metadata")