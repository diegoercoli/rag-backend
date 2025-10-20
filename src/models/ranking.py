from sqlalchemy import Column, Integer, Boolean, Float, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from src.database import Base


class Ranking(Base):
    __tablename__ = "ranking"
    __table_args__ = (
        UniqueConstraint('experiment_id', 'query_id', 'rank_position',
                        name='ranking_unique_experiment_query_position'),
        Index('idx_ranking_chunk', 'chunk_id'),
        Index('idx_ranking_query', 'query_id'),
        Index('idx_ranking_experiment', 'experiment_id'),
        {'schema': 'retrieval_framework'}
    )

    id = Column(Integer, primary_key=True)
    rank_position = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)
    is_relevant = Column(Boolean)
    chunk_id = Column(
        Integer,
        ForeignKey('retrieval_framework.chunk.id', ondelete='CASCADE'),
        nullable=False
    )
    query_id = Column(
        Integer,
        ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'),
        nullable=False
    )
    experiment_id = Column(
        Integer,
        ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'),
        nullable=False
    )

    chunk = relationship("Chunk", back_populates="rankings")
    query = relationship("Query", back_populates="rankings")
    experiment = relationship("Experiment", back_populates="rankings")