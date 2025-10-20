from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ExperimentStatus

# Association table for many-to-many relationship between experiments and documents
experiment_document_association = Table(
    'experiment_document',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('document_id', Integer, ForeignKey('retrieval_framework.document.id', ondelete='CASCADE'),
           nullable=False),
    Column('experiment_id', Integer, ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'),
           nullable=False),
    Column('added_at', DateTime, server_default=func.now()),
    Column('hash', String(64), nullable=True),
    schema='retrieval_framework'
)


# SQLAlchemy ORM model for experiments
class Experiment(Base):
    __tablename__ = "experiment"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    data_ingestion_time = Column(Float, nullable=True)
    date_evaluation_time = Column(Float, nullable=True)
    configuration_id = Column(Integer, ForeignKey('retrieval_framework.configuration.id', ondelete='CASCADE'),
                              nullable=False)
    dataset_id = Column(Integer, ForeignKey('retrieval_framework.dataset.id', ondelete='CASCADE'), nullable=False)
    vector_db_collection_id = Column(Integer,
                                     ForeignKey('retrieval_framework.vector_db_collection.id', ondelete='RESTRICT'))

    status = Column(
        Enum(ExperimentStatus,
             name='experiment_status', schema='retrieval_framework'),
        nullable=False,
        server_default='NOT_STARTED'
    )

    error_message = Column(Text, nullable=True)  # Add this for crash details

    configuration = relationship("Configuration")
    dataset = relationship("Dataset")
    vector_db_collection = relationship("VectorDBCollection", back_populates="experiments")
    rankings = relationship("Ranking", back_populates="experiment")
    metrics = relationship("Metrics", back_populates="experiment")

    # Direct many-to-many relationship to documents (lazy loaded)
    documents = relationship(
        "Document",
        secondary=experiment_document_association,  # Fixed typo: esperiment -> experiment
        back_populates="experiments",  # Add this
        lazy='select'
    )

