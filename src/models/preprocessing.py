from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models import ChunkingType
# SQLAlchemy ORM model for preprocessing configurations
class Preprocessing(Base):
    __tablename__ = "preprocessing"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    lowercase = Column(Boolean, nullable=False)

    configurations = relationship("Configuration", back_populates="preprocessing")