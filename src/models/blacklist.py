from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint, Index, String
from sqlalchemy.orm import relationship
from src.database import Base


class Blacklist(Base):
    """
    N:N association table linking ingestion configurations with blacklisted chapters.

    This allows many-to-many relationship:
    - One ingestion configuration can have many blacklisted chapters
    - One blacklist chapter can be used by many ingestion configurations
    """
    __tablename__ = "blacklist"
    __table_args__ = (
        UniqueConstraint(
            'ingestion_configuration_id',
            'blacklist_chapter_id',
            name='blacklist_unique_pair'
        ),
        Index('idx_blacklist_ingestion_configuration', 'ingestion_configuration_id'),
        Index('idx_blacklist_chapter', 'blacklist_chapter_id'),
        {'schema': 'retrieval_framework'}
    )

    id = Column(Integer, primary_key=True)
    ingestion_configuration_id = Column(
        Integer,
        ForeignKey('retrieval_framework.ingestion_configuration.id', ondelete='CASCADE'),
        nullable=False
    )
    blacklist_chapter_id = Column(
        Integer,
        ForeignKey('retrieval_framework.blacklist_chapter.id', ondelete='CASCADE'),
        nullable=False
    )

    # Relationships - USE STRING REFERENCES
    ingestion_configuration = relationship(
        "IngestionConfiguration",  # ← String reference
        back_populates="blacklist_associations"
    )
    blacklist_chapter = relationship(
        "BlacklistChapter",  # ← String reference
        back_populates="blacklist_associations"
    )

    def __repr__(self):
        return (f"<Blacklist(id={self.id}, "
                f"ingestion_config_id={self.ingestion_configuration_id}, "
                f"blacklist_chapter_id={self.blacklist_chapter_id})>")

class BlacklistChapter(Base):
    __tablename__ = "blacklist_chapter"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    # Relationship to blacklist associations - USE STRING REFERENCE
    blacklist_associations = relationship(
        "Blacklist",  # ← String reference
        back_populates="blacklist_chapter",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<BlacklistChapter(id={self.id}, name='{self.name}')>"