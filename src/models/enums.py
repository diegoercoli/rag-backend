# Enums
import enum
from sqlalchemy import types, String, TypeDecorator
from sqlalchemy.dialects.postgresql import ENUM as PG_ENUM

class ResearchType(str, enum.Enum):
    KEYWORD = "Keyword"
    SEMANTIC = "Semantic"
    HYBRID = "Hybrid"


class ConfidenceLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"

    def __str__(self):
        return self.value



class ConfidenceLevelType(TypeDecorator):
    """
    Custom SQLAlchemy type for ConfidenceLevel enum that properly handles
    PostgreSQL native enum type while using Python enum values.
    """
    impl = PG_ENUM(
        'Low', 'Medium', 'High',
        name='confidence_level',
        schema='retrieval_framework',
        create_type=False  # Don't try to create the type, it already exists
    )
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Convert Python value to database value"""
        if value is None:
            return None
        if isinstance(value, ConfidenceLevel):
            return value.value  # Return 'Low', 'Medium', or 'High'
        if isinstance(value, str):
            # Validate it's a valid value
            try:
                ConfidenceLevel(value)
                return value
            except ValueError:
                # Maybe it's the enum name? Try to convert
                try:
                    return ConfidenceLevel[value.upper()].value
                except KeyError:
                    raise ValueError(f"Invalid confidence level: {value}")
        raise ValueError(f"Invalid confidence type: {type(value)}")

    def process_result_value(self, value, dialect):
        """Convert database value to Python value"""
        if value is None:
            return None
        return ConfidenceLevel(value)

    @property
    def python_type(self):
        return ConfidenceLevel

class ChunkingType(str, enum.Enum):
    HIERARCHICAL = "Hierarchical"

class ComplexityQuery(str, enum.Enum):
    Textual_Description = "Textual_Description"
    IMAGE_ANALYSIS = "Image_Analysis"
    TABLE_ANALYSIS = "Table_Analysis"
    REASONING = "Reasoning"
    ''''
    Textual_Description = enum.auto(), # = "Textual_Description"
    Image_Analysis = enum.auto(),
    Table_Analysis = enum.auto(),
    Reasoning = enum.auto()
    '''

class ExperimentStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_EXECUTION = "IN_EXECUTION"
    ENDED = "ENDED"
    ABORTED = "ABORTED"
    CRASHED = "CRASHED"

