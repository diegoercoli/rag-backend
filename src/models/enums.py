# Enums
import enum


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

class ExperimentStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_EXECUTION = "IN_EXECUTION"
    ENDED = "ENDED"
    ABORTED = "ABORTED"
    CRASHED = "CRASHED"

