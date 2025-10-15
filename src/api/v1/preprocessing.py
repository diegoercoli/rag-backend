from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.preprocessing import Preprocessing
from src.schemas.preprocessing import PreprocessingCreate, PreprocessingResponse

router = APIRouter()

@router.get("/", response_model=List[PreprocessingResponse])
async def list_preprocessing(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all preprocessing configurations"""
    result = await db.execute(
        select(Preprocessing).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=PreprocessingResponse, status_code=201)
async def create_preprocessing(
    preprocessing: PreprocessingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create preprocessing configuration"""
    db_preprocessing = Preprocessing(**preprocessing.dict())
    db.add(db_preprocessing)
    await db.commit()
    await db.refresh(db_preprocessing)
    return db_preprocessing

@router.get("/{preprocessing_id}", response_model=PreprocessingResponse)
async def get_preprocessing(
    preprocessing_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get preprocessing details"""
    result = await db.execute(
        select(Preprocessing).where(Preprocessing.id == preprocessing_id)
    )
    preprocessing = result.scalar_one_or_none()
    if not preprocessing:
        raise HTTPException(status_code=404, detail="Preprocessing not found")
    return preprocessing

@router.put("/{preprocessing_id}", response_model=PreprocessingResponse)
async def update_preprocessing(
    preprocessing_id: int,
    preprocessing_update: PreprocessingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update preprocessing configuration"""
    result = await db.execute(
        select(Preprocessing).where(Preprocessing.id == preprocessing_id)
    )
    preprocessing = result.scalar_one_or_none()
    if not preprocessing:
        raise HTTPException(status_code=404, detail="Preprocessing not found")
    
    for field, value in preprocessing_update.dict().items():
        setattr(preprocessing, field, value)
    
    await db.commit()
    await db.refresh(preprocessing)
    return preprocessing

@router.delete("/{preprocessing_id}", status_code=204)
async def delete_preprocessing(
    preprocessing_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete preprocessing configuration"""
    result = await db.execute(
        select(Preprocessing).where(Preprocessing.id == preprocessing_id)
    )
    preprocessing = result.scalar_one_or_none()
    if not preprocessing:
        raise HTTPException(status_code=404, detail="Preprocessing not found")
    
    await db.delete(preprocessing)
    await db.commit()

# ============================================================================
