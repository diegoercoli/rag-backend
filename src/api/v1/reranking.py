from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.reranking import Reranking
from src.schemas.reranking import RerankingResponse, RerankingCreate

router = APIRouter()


@router.get("/", response_model=List[RerankingResponse])
async def list_reranking(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all reranking models"""
    result = await db.execute(
        select(Reranking).offset(skip).limit(limit)
    )
    return result.scalars().all()



@router.post("/", response_model=RerankingResponse, status_code=201)
async def create_reranking(
    reranking: RerankingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create reranking model"""
    db_reranking = Reranking(**reranking.dict())
    db.add(db_reranking)
    await db.commit()
    await db.refresh(db_reranking)
    return db_reranking

@router.get("/{reranking_id}", response_model=RerankingResponse)
async def get_reranking(
    reranking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get reranking details"""
    result = await db.execute(
        select(Reranking).where(Reranking.id == reranking_id)
    )
    reranking = result.scalar_one_or_none()
    if not reranking:
        raise HTTPException(status_code=404, detail="Reranking not found")
    return reranking

@router.put("/{reranking_id}", response_model=RerankingResponse)
async def update_reranking(
    reranking_id: int,
    reranking_update: RerankingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update reranking model"""
    result = await db.execute(
        select(Reranking).where(Reranking.id == reranking_id)
    )
    reranking = result.scalar_one_or_none()
    if not reranking:
        raise HTTPException(status_code=404, detail="Reranking not found")
    
    for field, value in reranking_update.dict().items():
        setattr(reranking, field, value)
    
    await db.commit()
    await db.refresh(reranking)
    return reranking

@router.delete("/{reranking_id}", status_code=204)
async def delete_reranking(
    reranking_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete reranking model"""
    result = await db.execute(
        select(Reranking).where(Reranking.id == reranking_id)
    )
    reranking = result.scalar_one_or_none()
    if not reranking:
        raise HTTPException(status_code=404, detail="Reranking not found")
    
    await db.delete(reranking)
    await db.commit()

# ============================================================================
