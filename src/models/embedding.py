from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

# SQLAlchemy ORM model for embeddings
class Embedding(Base):
    __tablename__ = "embedding"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), unique=True, nullable=False)
    max_input_tokens = Column(Integer, nullable=False)

    # No relationship back to Configuration
    #configurations = relationship("Configuration", back_populates="embedding")