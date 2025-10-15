from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum, Table
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base
# SQLAlchemy ORM model for blacklisted documents/queries
class BlacklistChapter(Base):
    __tablename__ = "blacklist_chapter"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    #blacklist = relationship("Blacklist", back_populates="blacklist_chapter")

# --- Association Table (no ORM class needed) ---
blacklist_association = Table(
    "blacklist",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("configuration_id", Integer, ForeignKey("retrieval_framework.configuration.id", ondelete="CASCADE")),
    Column("blacklist_chapter_id", Integer, ForeignKey("retrieval_framework.blacklist_chapter.id", ondelete="CASCADE")),
    schema="retrieval_framework"
)


'''
class Blacklist(Base):
    __tablename__ = "blacklist"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    configuration_id = Column(Integer, ForeignKey('retrieval_framework.configuration.id', ondelete='CASCADE'),
                              nullable=False)
    blacklist_chapter_id = Column(Integer, ForeignKey('retrieval_framework.blacklist_chapter.id', ondelete='CASCADE'),
                                  nullable=False)

    configuration = relationship("Configuration", back_populates="blacklist")
    blacklist_chapter = relationship("BlacklistChapter", back_populates="blacklist")
'''
