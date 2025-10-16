from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base


# Enums
class ResearchType(str, enum.Enum):
    KEYWORD = "Keyword"
    SEMANTIC = "Semantic"
    HYBRID = "Hybrid"

class ConfidenceLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

class ChunkingType(str, enum.Enum):
    HIERARCHICAL = "Hierarchical"

class ComplexityQuery(str, enum.Enum):
    TEXTUAL_DESCRIPTION = "Textual_Description"
    IMAGE_ANALYSIS = "Image_Analysis"
    TABLE_ANALYSIS = "Table_Analysis"
    REASONING = "Reasoning"

# Import all models to ensure they're registered with SQLAlchemy
# This must happen AFTER Base is defined but BEFORE any relationships are resolved
from src.models.blacklist import BlacklistChapter, blacklist_association
from src.models.embedding import Embedding
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
from src.models.knowledge_base import knowledge_base_association
from src.models.experiment import Experiment
from src.models.ranking import Ranking
from src.models.metrics import Metrics
from src.models.vector_db import VectorDBProvider, VectorDBCollection

# Make all models available when importing from src.models
__all__ = [
    'Base',
    'ConfidenceLevel',
    'ChunkingType',
    'ComplexityQuery',
    'BlacklistChapter',
    'blacklist_association',
    'Embedding',
    'Reranking',
    'Chunking',
    'QueryEnhancement',
    'Preprocessing',
    'ResearchStrategy',
    'Configuration',
    'Dataset',
    'HierarchicalMetadata',
    'Chunk',
    'Query',
    'GroundTruth',
    'Document',
    'knowledge_base_association',
    'Experiment',
    'Ranking',
    'Metrics',
    'VectorDBProvider',
    'VectorDBCollection',
]