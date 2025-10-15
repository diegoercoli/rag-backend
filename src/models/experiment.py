from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models.knowledge_base import knowledge_base_association


# SQLAlchemy ORM model for experiments
class Experiment(Base):
    __tablename__ = "experiment"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    data_ingestion_time = Column(Float, nullable=True)
    date_evaluation_time = Column(Float, nullable=True)
    configuration_id = Column(Integer, ForeignKey('retrieval_framework.configuration.id', ondelete='CASCADE'),
                              nullable=False)
    dataset_id = Column(Integer, ForeignKey('retrieval_framework.dataset.id', ondelete='CASCADE'), nullable=False)
    vector_db_collection_id = Column(Integer,
                                     ForeignKey('retrieval_framework.vector_db_collection.id', ondelete='RESTRICT'))

    configuration = relationship("Configuration", back_populates="experiments")
    dataset = relationship("Dataset", back_populates="experiments")
    vector_db_collection = relationship("VectorDBCollection", back_populates="experiments")
    rankings = relationship("Ranking", back_populates="experiment")
    metrics = relationship("Metrics", back_populates="experiment")
    #knowledge_base = relationship("KnowledgeBase", back_populates="experiment")
    # Direct many-to-many relationship to documents (lazy loaded)
    documents = relationship(
        "Document",
        secondary=knowledge_base_association,
        lazy='select'  # lazy loading
    )