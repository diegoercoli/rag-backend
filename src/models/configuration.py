from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
from src.models.blacklist import blacklist_association


class Configuration(Base):
    __tablename__ = "configuration"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    idconfiguration = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    embedding_id = Column(Integer, ForeignKey('retrieval_framework.embedding.id', ondelete='RESTRICT'))
    reranking_id = Column(Integer, ForeignKey('retrieval_framework.reranking.id', ondelete='RESTRICT'))
    chunking_id = Column(Integer, ForeignKey('retrieval_framework.chunking.id', ondelete='RESTRICT'))
    query_enhancement_id = Column(Integer, ForeignKey('retrieval_framework.query_enhancement.id', ondelete='RESTRICT'))
    preprocessing_id = Column(Integer, ForeignKey('retrieval_framework.preprocessing.id', ondelete='RESTRICT'))
    research_strategy_id = Column(Integer, ForeignKey('retrieval_framework.research_strategy.id', ondelete='RESTRICT'))

    embedding = relationship("Embedding")#, back_populates="configurations")
    reranking = relationship("Reranking", back_populates="configurations")
    chunking = relationship("Chunking", back_populates="configurations")
    query_enhancement = relationship("QueryEnhancement", back_populates="configurations")
    preprocessing = relationship("Preprocessing", back_populates="configurations")
    research_strategy = relationship("ResearchStrategy", back_populates="configurations")
    experiments = relationship("Experiment", back_populates="configuration")
    #blacklist = relationship("Blacklist", back_populates="configuration")
    # direct relationship to BlacklistChapter via association table
    blacklist_chapters = relationship(
        "BlacklistChapter",
        secondary=blacklist_association,
        cascade="all, delete",
        lazy="joined"  #fetched eagerly
    )