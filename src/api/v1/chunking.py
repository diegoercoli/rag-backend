from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.chunking import Chunking
from src.schemas.chunking import ChunkingCreate, ChunkingResponse

router = APIRouter()

@router.get("/", response_model=List[ChunkingResponse])
async def list_chunking(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all chunking configurations"""
    result = await db.execute(
        select(Chunking).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=ChunkingResponse, status_code=201)
async def create_chunking(
    chunking: ChunkingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create chunking configuration"""
    db_chunking = Chunking(**chunking.dict())
    db.add(db_chunking)
    await db.commit()
    await db.refresh(db_chunking)
    return db_chunking

@router.get("/{chunking_id}", response_model=ChunkingResponse)
async def get_chunking(
    chunking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get chunking details"""
    result = await db.execute(
        select(Chunking).where(Chunking.id == chunking_id)
    )
    chunking = result.scalar_one_or_none()
    if not chunking:
        raise HTTPException(status_code=404, detail="Chunking not found")
    return chunking

@router.put("/{chunking_id}", response_model=ChunkingResponse)
async def update_chunking(
    chunking_id: int,
    chunking_update: ChunkingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update chunking configuration"""
    result = await db.execute(
        select(Chunking).where(Chunking.id == chunking_id)
    )
    chunking = result.scalar_one_or_none()
    if not chunking:
        raise HTTPException(status_code=404, detail="Chunking not found")
    
    for field, value in chunking_update.dict().items():
        setattr(chunking, field, value)
    
    await db.commit()
    await db.refresh(chunking)
    return chunking

@router.delete("/{chunking_id}", status_code=204)
async def delete_chunking(
    chunking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete chunking configuration"""
    result = await db.execute(
        select(Chunking).where(Chunking.id == chunking_id)
    )
    chunking = result.scalar_one_or_none()
    if not chunking:
        raise HTTPException(status_code=404, detail="Chunking not found")
    
    await db.delete(chunking)
    await db.commit()

# ============================================================================
