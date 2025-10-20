from sqlalchemy import (
    Column, Integer, String, Boolean, Text, ForeignKey, Enum,
    UniqueConstraint, Index, DateTime, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base
from src.models import ComplexityQuery
from src.models.enums import ComplexityQueryType

# Association table for N:N relationship (now much simpler!)
query_ground_truth_association = Table(
    'query_ground_truth',
    Base.metadata,
    Column('query_id', Integer, ForeignKey('retrieval_framework.query.id', ondelete='CASCADE'),
           nullable=False, primary_key=True),
    Column('ground_truth_id', Integer, ForeignKey('retrieval_framework.ground_truth.id', ondelete='CASCADE'),
           nullable=False, primary_key=True),
    schema='retrieval_framework'
)


class Query(Base):
    __tablename__ = "query"
    __table_args__ = (
        UniqueConstraint('position_id', 'dataset_id', 'version',
                         name='query_unique_position_dataset_version'),
        Index('idx_query_dataset', 'dataset_id'),
        Index('idx_query_position', 'position_id', 'dataset_id'),
        Index('idx_query_obsolete', 'dataset_id', 'obsolete'),
        Index('idx_query_version', 'position_id', 'dataset_id', 'version'),
        Index('idx_query_created_at', 'created_at'),
        {'schema': 'retrieval_framework'}
    )

    id = Column(Integer, primary_key=True, autoincrement=True,
                comment='Auto-increment primary key')
    position_id = Column(Integer, nullable=False,
                         comment='Relative position of query within the dataset')
    dataset_id = Column(
        Integer,
        ForeignKey('retrieval_framework.dataset.id', ondelete='CASCADE'),
        nullable=False
    )
    version = Column(Integer, nullable=False, comment='Version number of the query')
    prompt = Column(Text, nullable=False)
    device = Column(String(255))
    customer = Column(String(255))
    obsolete = Column(Boolean, nullable=False, default=False)
    complexity = Column(ComplexityQueryType(), nullable=False)
   #     Enum(ComplexityQuery, name="complexity_query", schema="retrieval_framework"),
   #     nullable=False
   # )
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    # Relationships (now much simpler!)
    dataset = relationship("Dataset", back_populates="queries")
    rankings = relationship("Ranking", back_populates="query", cascade="all, delete-orphan")
    metrics = relationship("Metrics", back_populates="query", cascade="all, delete-orphan")

    # N:N relationship with GroundTruth
    ground_truths = relationship(
        "GroundTruth",
        secondary="retrieval_framework.query_ground_truth"#,
      #  back_populates="queries"
    )


