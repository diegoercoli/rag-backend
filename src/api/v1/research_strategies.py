from fastapi import APIRouter

from src.models.research_strategy import ResearchStrategy
from src.schemas.research_strategy import ResearchStrategyCreate, ResearchStrategyResponse
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.models.ranking import Ranking
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse
from src.schemas.ranking import RankingResponse
router = APIRouter()

@router.get("/", response_model=List[ResearchStrategyResponse])
async def list_research_strategies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all research strategies"""
    result = await db.execute(
        select(ResearchStrategy).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=ResearchStrategyResponse, status_code=201)
async def create_research_strategy(
    strategy: ResearchStrategyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create research strategy"""
    db_strategy = ResearchStrategy(**strategy.dict())
    db.add(db_strategy)
    await db.commit()
    await db.refresh(db_strategy)
    return db_strategy

@router.get("/{strategy_id}", response_model=ResearchStrategyResponse)
async def get_research_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get research strategy details"""
    result = await db.execute(
        select(ResearchStrategy).where(ResearchStrategy.id == strategy_id)
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Research strategy not found")
    return strategy

@router.put("/{strategy_id}", response_model=ResearchStrategyResponse)
async def update_research_strategy(
    strategy_id: int,
    strategy_update: ResearchStrategyCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update research strategy"""
    result = await db.execute(
        select(ResearchStrategy).where(ResearchStrategy.id == strategy_id)
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Research strategy not found")
    
    for field, value in strategy_update.dict().items():
        setattr(strategy, field, value)
    
    await db.commit()
    await db.refresh(strategy)
    return strategy

@router.delete("/{strategy_id}", status_code=204)
async def delete_research_strategy(
    strategy_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete research strategy"""
    result = await db.execute(
        select(ResearchStrategy).where(ResearchStrategy.id == strategy_id)
    )
    strategy = result.scalar_one_or_none()
    if not strategy:
        raise HTTPException(status_code=404, detail="Research strategy not found")
    
    await db.delete(strategy)
    await db.commit()

# ============================================================================
