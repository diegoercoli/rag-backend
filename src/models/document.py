# SQLAlchemy ORM model for documents
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
class Document(Base):
    __tablename__ = "document"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    version = Column(Float, nullable=False)
    type = Column(String(100), nullable=False)
    hash = Column(String(64), unique=True, nullable=False)
    filename = Column(String(500), nullable=False)
    #knowledge_base = relationship("KnowledgeBase", back_populates="document")
