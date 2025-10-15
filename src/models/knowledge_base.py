from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

# SQLAlchemy ORM model for knowledge bases
# Define the association table (not an ORM class, just a Table)
knowledge_base_association = Table(
    'knowledge_base',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('document_id', Integer, ForeignKey('retrieval_framework.document.id', ondelete='CASCADE'), nullable=False),
    Column('experiment_id', Integer, ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'), nullable=False),
    Column('added_at', DateTime, server_default=func.now()),
    schema='retrieval_framework'
)


'''
class KnowledgeBase(Base):
    __tablename__ = "knowledge_base"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('retrieval_framework.document.id', ondelete='CASCADE'), nullable=False)
    experiment_id = Column(Integer, ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'), nullable=False)
    added_at = Column(DateTime, server_default=func.now())

    document = relationship("Document", back_populates="knowledge_base")
    experiment = relationship("Experiment", back_populates="knowledge_base")
'''

