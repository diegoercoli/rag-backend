from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class IngestionConfiguration(Base):
    __tablename__ = "ingestion_configuration"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    hashcode = Column(String(64), unique=True, nullable=False)
    embedding_id = Column(Integer, ForeignKey('retrieval_framework.embedding.id', ondelete='RESTRICT'), nullable=False)
    chunking_id = Column(Integer, ForeignKey('retrieval_framework.chunking.id', ondelete='RESTRICT'), nullable=False)
    preprocessing_id = Column(Integer, ForeignKey('retrieval_framework.preprocessing.id', ondelete='RESTRICT'), nullable=False)

    # Relationships
    embedding = relationship("Embedding")
    chunking = relationship("Chunking")
    preprocessing = relationship("Preprocessing")

    # Relationship to BlacklistChapter via association table
    blacklist_chapters = relationship(
        "BlacklistChapter",
        secondary=blacklist_association,
        cascade="all, delete",
        lazy="joined"
    )