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
    current_hash = Column(String(64), unique=True, nullable=False)
    filename = Column(String(500), nullable=False)
    knowledge_base_id = Column(
        Integer,
        ForeignKey('retrieval_framework.knowledge_base.id', ondelete='SET NULL'),
        nullable=True
    )
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    knowledge_base = relationship("KnowledgeBase", back_populates="documents")

    # Many-to-many relationship with experiments
    experiments = relationship(
        "Experiment",
        secondary="retrieval_framework.experiment_document",
        back_populates="documents",
        lazy='select'
    )
