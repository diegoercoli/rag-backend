from sqlalchemy import (
    Column, Integer, String, Boolean, Float, DateTime, Date, Text, ForeignKey, Enum
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

# Enums
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


