from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base


class Configuration(Base):
    __tablename__ = "configuration"
    __table_args__ = {'schema': 'retrieval_framework'}

    id = Column(Integer, primary_key=True)
    idconfiguration = Column(String(255), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    ingestion_configuration_id = Column(
        Integer,
        ForeignKey('retrieval_framework.ingestion_configuration.id', ondelete='RESTRICT'),
        nullable=True  # Make nullable if it can be null
    )
    retrieval_configuration_id = Column(
        Integer,
        ForeignKey('retrieval_framework.retrieval_configuration.id', ondelete='RESTRICT'),
        nullable=True  # Make nullable if it can be null
    )

    # Relationships with explicit foreign_keys parameter
    ingestion_configuration = relationship(
        "IngestionConfiguration",
        foreign_keys=[ingestion_configuration_id]#, back_populates="configurations"
    )
    retrieval_configuration = relationship(
        "RetrievalConfiguration",
        foreign_keys=[retrieval_configuration_id]#, back_populates="configurations"
    )