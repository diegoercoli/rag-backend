from sqlalchemy import Column, Integer, String, Table, ForeignKey
from src.database import Base

# SQLAlchemy ORM model for blacklisted chapters
class BlacklistChapter(Base):
    __tablename__ = "blacklist_chapter"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


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