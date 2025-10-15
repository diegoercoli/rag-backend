from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.query_enhancement import QueryEnhancement
from src.schemas.query_enhancement import QueryEnhancementCreate, QueryEnhancementResponse

router = APIRouter()

@router.get("/", response_model=List[QueryEnhancementResponse])
async def list_query_enhancement(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all query enhancement configurations"""
    result = await db.execute(
        select(QueryEnhancement).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=QueryEnhancementResponse, status_code=201)
async def create_query_enhancement(
    enhancement: QueryEnhancementCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create query enhancement configuration"""
    db_enhancement = QueryEnhancement(**enhancement.dict())
    db.add(db_enhancement)
    await db.commit()
    await db.refresh(db_enhancement)
    return db_enhancement

@router.get("/{enhancement_id}", response_model=QueryEnhancementResponse)
async def get_query_enhancement(
    enhancement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get query enhancement details"""
    result = await db.execute(
        select(QueryEnhancement).where(QueryEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()
    if not enhancement:
        raise HTTPException(status_code=404, detail="Query enhancement not found")
    return enhancement

@router.put("/{enhancement_id}", response_model=QueryEnhancementResponse)
async def update_query_enhancement(
    enhancement_id: int,
    enhancement_update: QueryEnhancementCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update query enhancement configuration"""
    result = await db.execute(
        select(QueryEnhancement).where(QueryEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()
    if not enhancement:
        raise HTTPException(status_code=404, detail="Query enhancement not found")
    
    for field, value in enhancement_update.dict().items():
        setattr(enhancement, field, value)
    
    await db.commit()
    await db.refresh(enhancement)
    return enhancement

@router.delete("/{enhancement_id}", status_code=204)
async def delete_query_enhancement(
    enhancement_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete query enhancement configuration"""
    result = await db.execute(
        select(QueryEnhancement).where(QueryEnhancement.id == enhancement_id)
    )
    enhancement = result.scalar_one_or_none()
    if not enhancement:
        raise HTTPException(status_code=404, detail="Query enhancement not found")
    
    await db.delete(enhancement)
    await db.commit()
    
# ============================================================================
