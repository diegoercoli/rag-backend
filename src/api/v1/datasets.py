from fastapi import APIRouter

from src.models.dataset import Dataset
from src.models.query import Query
from src.schemas.dataset import DatasetCreate, DatasetUpdate, DatasetResponse
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.query import QueryResponse

router = APIRouter()

@router.get("/", response_model=List[DatasetResponse])
async def list_datasets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all datasets"""
    result = await db.execute(
        select(Dataset).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=DatasetResponse, status_code=201)
async def create_dataset(
    dataset: DatasetCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new dataset"""
    db_dataset = Dataset(**dataset.dict())
    db.add(db_dataset)
    await db.commit()
    await db.refresh(db_dataset)
    return db_dataset

@router.get("/{dataset_id}", response_model=DatasetResponse)
async def get_dataset(
    dataset_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get dataset by ID"""
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return dataset

@router.patch("/{dataset_id}", response_model=DatasetResponse)
async def update_dataset(
    dataset_id: int,
    dataset_update: DatasetUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update dataset"""
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    for field, value in dataset_update.dict(exclude_unset=True).items():
        setattr(dataset, field, value)
    
    await db.commit()
    await db.refresh(dataset)
    return dataset

@router.delete("/{dataset_id}", status_code=204)
async def delete_dataset(
    dataset_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete dataset"""
    result = await db.execute(
        select(Dataset).where(Dataset.id == dataset_id)
    )
    dataset = result.scalar_one_or_none()
    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    await db.delete(dataset)
    await db.commit()

@router.get("/{dataset_id}/queries", response_model=List[QueryResponse])
async def get_dataset_queries(
    dataset_id: int,
    obsolete: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get all queries in a dataset"""
    query = select(Query).where(Query.dataset_id == dataset_id)
    if obsolete is not None:
        query = query.where(Query.obsolete == obsolete)
    
    result = await db.execute(query)
    return result.scalars().all()

# ============================================================================
