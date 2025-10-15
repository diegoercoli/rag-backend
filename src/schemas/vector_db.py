from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class VectorDBProviderBase(BaseModel):
    name: str
    port_number: int

class VectorDBProviderCreate(VectorDBProviderBase):
    pass

class VectorDBProviderResponse(VectorDBProviderBase):
    id: int
    
    class Config:
        from_attributes = True

class VectorDBCollectionBase(BaseModel):
    collection_name: str
    provider_id: int

class VectorDBCollectionCreate(VectorDBCollectionBase):
    pass

class VectorDBCollectionResponse(VectorDBCollectionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# ============================================================================
