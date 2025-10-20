from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from src.database import Base


# --- Association Table (now pointing to ingestion_configuration instead of configuration) ---
blacklist_association = Table(
    "blacklist",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("ingestion_configuration_id", Integer,
           ForeignKey("retrieval_framework.ingestion_configuration.id", ondelete="CASCADE"),
           nullable=False),
    Column("blacklist_chapter_id", Integer,
           ForeignKey("retrieval_framework.blacklist_chapter.id", ondelete="CASCADE"),
           nullable=False),
    schema="retrieval_framework"
)

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