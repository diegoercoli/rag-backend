from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

# SQLAlchemy ORM model for vector database connections
class VectorDBProvider(Base):
    __tablename__ = "vector_db_provider"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    port_number = Column(Integer, nullable=False)

    collections = relationship("VectorDBCollection", back_populates="provider")


class VectorDBCollection(Base):
    __tablename__ = "vector_db_collection"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    collection_name = Column(String(255), unique=True, nullable=False)
    provider_id = Column(Integer, ForeignKey('retrieval_framework.vector_db_provider.id', ondelete='RESTRICT'),
                         nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    provider = relationship("VectorDBProvider", back_populates="collections")
    experiments = relationship("Experiment", back_populates="vector_db_collection")
