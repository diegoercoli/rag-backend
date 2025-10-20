from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import ConfidenceLevel
from src.models.enums import ConfidenceLevelType

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


class GroundTruth(Base):
    __tablename__ = "ground_truth"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    hierarchical_metadata_id = Column(
        Integer,
        ForeignKey('retrieval_framework.hierarchical_metadata.id', ondelete='SET NULL')
    )
    confidence = Column(ConfidenceLevelType(), nullable=False)  # ← Use custom type


    hierarchical_metadata = relationship("HierarchicalMetadata")

    # N:N relationship with Query
    queries = relationship(
        "Query",
        secondary="retrieval_framework.query_ground_truth",
        back_populates="ground_truths"
    )