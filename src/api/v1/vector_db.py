from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.experiment import Experiment
from src.models.vector_db import VectorDBProvider, VectorDBCollection
from src.schemas.vector_db import VectorDBProviderResponse, VectorDBProviderCreate, VectorDBCollectionResponse, \
    VectorDBCollectionCreate

router = APIRouter()

# Provider endpoints
@router.get("/providers", response_model=List[VectorDBProviderResponse])
async def list_providers(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all vector DB providers"""
    result = await db.execute(
        select(VectorDBProvider).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/providers", response_model=VectorDBProviderResponse, status_code=201)
async def create_provider(
    provider: VectorDBProviderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create vector DB provider"""
    db_provider = VectorDBProvider(**provider.dict())
    db.add(db_provider)
    await db.commit()
    await db.refresh(db_provider)
    return db_provider

@router.get("/providers/{provider_id}", response_model=VectorDBProviderResponse)
async def get_provider(
    provider_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get provider details"""
    result = await db.execute(
        select(VectorDBProvider).where(VectorDBProvider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.put("/providers/{provider_id}", response_model=VectorDBProviderResponse)
async def update_provider(
    provider_id: int,
    provider_update: VectorDBProviderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update provider"""
    result = await db.execute(
        select(VectorDBProvider).where(VectorDBProvider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    for field, value in provider_update.dict().items():
        setattr(provider, field, value)
    
    await db.commit()
    await db.refresh(provider)
    return provider

@router.delete("/providers/{provider_id}", status_code=204)
async def delete_provider(
    provider_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete provider"""
    result = await db.execute(
        select(VectorDBProvider).where(VectorDBProvider.id == provider_id)
    )
    provider = result.scalar_one_or_none()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    
    await db.delete(provider)
    await db.commit()

# Collection endpoints
@router.get("/collections", response_model=List[VectorDBCollectionResponse])
async def list_collections(
    provider_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all collections"""
    query = select(VectorDBCollection)
    if provider_id:
        query = query.where(VectorDBCollection.provider_id == provider_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/collections", response_model=VectorDBCollectionResponse, status_code=201)
async def create_collection(
    collection: VectorDBCollectionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create collection"""
    db_collection = VectorDBCollection(**collection.dict())
    db.add(db_collection)
    await db.commit()
    await db.refresh(db_collection)
    return db_collection

@router.get("/collections/{collection_id}", response_model=VectorDBCollectionResponse)
async def get_collection(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get collection details"""
    result = await db.execute(
        select(VectorDBCollection).where(VectorDBCollection.id == collection_id)
    )
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return collection

@router.delete("/collections/{collection_id}", status_code=204)
async def delete_collection(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete collection"""
    result = await db.execute(
        select(VectorDBCollection).where(VectorDBCollection.id == collection_id)
    )
    collection = result.scalar_one_or_none()
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    await db.delete(collection)
    await db.commit()

@router.get("/collections/{collection_id}/statistics")
async def get_collection_statistics(
    collection_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get collection statistics"""
    # Count experiments using this collection
    exp_count = await db.execute(
        select(func.count(Experiment.id)).where(
            Experiment.vector_db_collection_id == collection_id
        )
    )
    
    return {
        "collection_id": collection_id,
        "experiments_count": exp_count.scalar()
    }

# ============================================================================
