# SQLAlchemy ORM model for reranking results
from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base


class Reranking(Base):
    __tablename__ = "reranking"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), unique=True, nullable=False)
    max_input_tokens = Column(Integer, nullable=False)

    configurations = relationship("Configuration", back_populates="reranking")