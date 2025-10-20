from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class RetrievalConfiguration(Base):
    __tablename__ = "retrieval_configuration"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    hashcode = Column(String(64), unique=True, nullable=False)
    reranking_id = Column(Integer, ForeignKey('retrieval_framework.reranking.id', ondelete='RESTRICT'), nullable=False)
    query_enhancement_id = Column(Integer, ForeignKey('retrieval_framework.query_enhancement.id', ondelete='RESTRICT'))
    research_strategy_id = Column(Integer, ForeignKey('retrieval_framework.research_strategy.id', ondelete='RESTRICT'), nullable=False)

    # Relationships
    reranking = relationship("Reranking")
    query_enhancement = relationship("QueryEnhancement")
    research_strategy = relationship("ResearchStrategy")