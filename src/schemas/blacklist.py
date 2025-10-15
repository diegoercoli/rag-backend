from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlacklistChapterBase(BaseModel):
    name: str

class BlacklistChapterCreate(BlacklistChapterBase):
    pass

class BlacklistChapterResponse(BlacklistChapterBase):
    id: int
    
    class Config:
        from_attributes = True

class BlacklistEntryCreate(BaseModel):
    configuration_id: int
    blacklist_chapter_id: int

# ============================================================================
