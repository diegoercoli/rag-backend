from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Table, DateTime, func
from sqlalchemy.orm import relationship
from src.database import Base
from src.models import ConfidenceLevel
from src.models.enums import ConfidenceLevelType



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

    # Add these if missing:
    #query_id = Column(Integer, ForeignKey('retrieval_framework.query.id'))
   # created_at = Column(DateTime(timezone=True), server_default=func.now())

    hierarchical_metadata = relationship("HierarchicalMetadata")

    # N:N relationship with Query
 #   queries = relationship(
 #       "Query",
 #       secondary="retrieval_framework.query_ground_truth"#,
       # back_populates="ground_truths"
#    )