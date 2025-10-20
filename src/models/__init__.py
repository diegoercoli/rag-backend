# Import all models to ensure they're registered with SQLAlchemy
# This must happen AFTER Base is defined but BEFORE any relationships are resolved
from src.database import Base
from src.models.blacklist import BlacklistChapter
from src.models.embedding import Embedding
from src.models.enums import ChunkingType, ConfidenceLevel, ResearchType, ComplexityQuery, ExperimentStatus, \
    ConfidenceLevelType
from src.models.ingestion_configuration import IngestionConfiguration
from src.models.reranking import Reranking
from src.models.chunking import Chunking
from src.models.query_enhancement import QueryEnhancement
from src.models.preprocessing import Preprocessing
from src.models.research_strategy import ResearchStrategy
from src.models.configuration import Configuration
from src.models.dataset import Dataset
from src.models.hierarchical_metadata import HierarchicalMetadata
from src.models.chunk import Chunk
from src.models.query import Query
from src.models.ground_truth import GroundTruth
from src.models.document import Document
from src.models.knowledge_base import KnowledgeBase
from src.models.experiment import Experiment, experiment_document_association
from src.models.ranking import Ranking
from src.models.metrics import Metrics
from src.models.retrieval_configuration import RetrievalConfiguration
from src.models.vector_db import VectorDBProvider, VectorDBCollection

# Make all models available when importing from src.models
__all__ = [
    'Base',
    'ResearchType',
    'ConfidenceLevel',
    'ConfidenceLevelType',
    'ChunkingType',
    'ComplexityQuery',
    'ExperimentStatus',
    'BlacklistChapter',
  #  'blacklist_association',
    'Embedding',
    'Reranking',
    'Chunking',
    'QueryEnhancement',
    'Preprocessing',
    'ResearchStrategy',
    'IngestionConfiguration',  # NEW
    'RetrievalConfiguration',  # NEW
    'Configuration',
    'Dataset',
    'HierarchicalMetadata',
    'Chunk',
    'Query',
    'GroundTruth',
    'Document',
    'KnowledgeBase',
    'experiment_document_association',
    'Experiment',
    'Ranking',
    'Metrics',
    'VectorDBProvider',
    'VectorDBCollection',
]