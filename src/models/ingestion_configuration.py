from sqlalchemy import Column, Integer, String, ForeignKey, Index
from sqlalchemy.orm import relationship
from src.database import Base


class IngestionConfiguration(Base):
    __tablename__ = "ingestion_configuration"
    __table_args__ = (
        Index('idx_ingestion_configuration_embedding', 'embedding_id'),
        Index('idx_ingestion_configuration_chunking', 'chunking_id'),
        Index('idx_ingestion_configuration_preprocessing', 'preprocessing_id'),
        {'schema': 'retrieval_framework'}
    )

    id = Column(Integer, primary_key=True)
    hashcode = Column(String(64), nullable=False, unique=True)
    embedding_id = Column(
        Integer,
        ForeignKey('retrieval_framework.embedding.id', ondelete='RESTRICT'),
        nullable=False
    )
    chunking_id = Column(
        Integer,
        ForeignKey('retrieval_framework.chunking.id', ondelete='RESTRICT'),
        nullable=False
    )
    preprocessing_id = Column(
        Integer,
        ForeignKey('retrieval_framework.preprocessing.id', ondelete='RESTRICT'),
        nullable=False
    )

    # Relationships - USE STRING REFERENCES to avoid circular imports
    embedding = relationship("Embedding")#, back_populates="ingestion_configurations")
    chunking = relationship("Chunking")#, back_populates="ingestion_configurations")
    preprocessing = relationship("Preprocessing")#, back_populates="ingestion_configurations")
    configurations = relationship("Configuration")#, back_populates="ingestion_configuration")

    # N:N relationship with BlacklistChapter through Blacklist association
    # USE STRING REFERENCE: "Blacklist" instead of Blacklist
    blacklist_associations = relationship(
        "Blacklist",  # ← String reference
        back_populates="ingestion_configuration",
        cascade="all, delete-orphan"
    )

    # Convenience property to access blacklisted chapters directly
    @property
    def blacklisted_chapters(self):
        """Get list of blacklisted chapter names"""
        return [assoc.blacklist_chapter.name for assoc in self.blacklist_associations]

    def __repr__(self):
        return f"<IngestionConfiguration(id={self.id}, hashcode='{self.hashcode}')>"