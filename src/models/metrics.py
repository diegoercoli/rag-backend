from sqlalchemy import Column, Integer, Float, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from src.database import Base


class Metrics(Base):
    __tablename__ = "metrics"
    __table_args__ = (
        UniqueConstraint('experiment_id', 'query_id',
                        name='metrics_unique_experiment_query'),
        Index('idx_metrics_experiment', 'experiment_id'),
        Index('idx_metrics_query', 'query_id'),
        {'schema': 'retrieval_framework'}
    )

    id = Column(Integer, primary_key=True)
    precision_value = Column(Float)
    recall = Column(Float)
    f1_score = Column(Float)
    ndcg = Column(Float)
    mrr = Column(Float)
    map_value = Column(Float)
    experiment_id = Column(
        Integer,
        ForeignKey('retrieval_framework.experiment.id', ondelete='CASCADE'),
        nullable=False
    )
    query_id = Column(
        Integer,
        ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'),
        nullable=False
    )

    experiment = relationship("Experiment", back_populates="metrics")
    query = relationship("Query", back_populates="metrics")