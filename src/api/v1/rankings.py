from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.models.ranking import Ranking
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse
from src.schemas.ranking import RankingResponse
from src.schemas.ranking import RankingCreate, RankingUpdate, RankingBulkCreate

router = APIRouter()

@router.get("/", response_model=List[RankingResponse])
async def list_rankings(
    experiment_id: Optional[int] = None,
    query_id: Optional[int] = None,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Get rankings with filters"""
    query = select(Ranking)
    
    if experiment_id:
        query = query.where(Ranking.experiment_id == experiment_id)
    if query_id:
        query = query.where(Ranking.query_id == query_id)
    
    query = query.order_by(Ranking.rank_position).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=RankingResponse, status_code=201)
async def create_ranking(
    ranking: RankingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create ranking from search results"""
    db_ranking = Ranking(**ranking.dict())
    db.add(db_ranking)
    await db.commit()
    await db.refresh(db_ranking)
    return db_ranking

@router.patch("/{ranking_id}", response_model=RankingResponse)
async def update_ranking(
    ranking_id: int,
    ranking_update: RankingUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update ranking relevance"""
    result = await db.execute(
        select(Ranking).where(Ranking.id == ranking_id)
    )
    ranking = result.scalar_one_or_none()
    if not ranking:
        raise HTTPException(status_code=404, detail="Ranking not found")
    
    for field, value in ranking_update.dict(exclude_unset=True).items():
        setattr(ranking, field, value)
    
    await db.commit()
    await db.refresh(ranking)
    return ranking

@router.post("/bulk", response_model=List[RankingResponse])
async def bulk_create_rankings(
    bulk_data: RankingBulkCreate,
    db: AsyncSession = Depends(get_db)
):
    """Bulk create rankings"""
    rankings = []
    for result in bulk_data.results:
        ranking = Ranking(
            experiment_id=bulk_data.experiment_id,
            query_id=bulk_data.query_id,
            **result
        )
        db.add(ranking)
        rankings.append(ranking)
    
    await db.commit()
    for ranking in rankings:
        await db.refresh(ranking)
    
    return rankings

# ============================================================================
