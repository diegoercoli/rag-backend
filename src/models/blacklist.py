from sqlalchemy import Column, Integer, String, Table, ForeignKey
from src.database import Base

# SQLAlchemy ORM model for blacklisted chapters
class BlacklistChapter(Base):
    __tablename__ = "blacklist_chapter"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

