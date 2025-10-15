from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.models.metrics import Metrics
from src.models.ranking import Ranking
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse

from sqlalchemy import func

from src.schemas.metrics import MetricsResponse, MetricsCreate

router = APIRouter()

@router.get("/", response_model=List[MetricsResponse])
async def list_metrics(
    experiment_id: Optional[int] = None,
    query_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get metrics with filters"""
    query = select(Metrics)
    
    if experiment_id:
        query = query.where(Metrics.experiment_id == experiment_id)
    if query_id:
        query = query.where(Metrics.query_id == query_id)
    
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/calculate", response_model=MetricsResponse)
async def calculate_metrics(
    metrics_data: MetricsCreate,
    db: AsyncSession = Depends(get_db)
):
    """Calculate and store metrics for a query in an experiment"""
    # Get rankings for this query/experiment
    rankings_result = await db.execute(
        select(Ranking).where(
            Ranking.experiment_id == metrics_data.experiment_id,
            Ranking.query_id == metrics_data.query_id
        ).order_by(Ranking.rank_position)
    )
    rankings = rankings_result.scalars().all()
    
    if not rankings:
        raise HTTPException(status_code=404, detail="No rankings found")
    
    # Calculate metrics
    relevant_count = sum(1 for r in rankings if r.is_relevant)
    total_count = len(rankings)
    
    precision = relevant_count / total_count if total_count > 0 else 0.0
    
    # Simple NDCG calculation (simplified)
    dcg = sum((1 if r.is_relevant else 0) / (i + 2) for i, r in enumerate(rankings))
    idcg = sum(1 / (i + 2) for i in range(relevant_count))
    ndcg = dcg / idcg if idcg > 0 else 0.0
    
    # MRR - position of first relevant result
    mrr = 0.0
    for i, r in enumerate(rankings):
        if r.is_relevant:
            mrr = 1.0 / (i + 1)
            break
    
    # Create metrics
    db_metrics = Metrics(
        experiment_id=metrics_data.experiment_id,
        query_id=metrics_data.query_id,
        precision_value=precision,
        recall=None,  # Need ground truth for recall
        f1_score=None,
        ndcg=ndcg,
        mrr=mrr,
        map_value=None
    )
    
    db.add(db_metrics)
    await db.commit()
    await db.refresh(db_metrics)
    return db_metrics

@router.get("/aggregate")
async def aggregate_metrics(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Aggregate metrics for an experiment"""
    result = await db.execute(
        select(
            func.avg(Metrics.precision_value).label('avg_precision'),
            func.avg(Metrics.recall).label('avg_recall'),
            func.avg(Metrics.f1_score).label('avg_f1'),
            func.avg(Metrics.ndcg).label('avg_ndcg'),
            func.avg(Metrics.mrr).label('avg_mrr'),
            func.avg(Metrics.map_value).label('avg_map'),
            func.count(Metrics.id).label('query_count')
        ).where(Metrics.experiment_id == experiment_id)
    )
    
    row = result.one()
    return {
        "experiment_id": experiment_id,
        "avg_precision": float(row.avg_precision) if row.avg_precision else None,
        "avg_recall": float(row.avg_recall) if row.avg_recall else None,
        "avg_f1": float(row.avg_f1) if row.avg_f1 else None,
        "avg_ndcg": float(row.avg_ndcg) if row.avg_ndcg else None,
        "avg_mrr": float(row.avg_mrr) if row.avg_mrr else None,
        "avg_map": float(row.avg_map) if row.avg_map else None,
        "query_count": row.query_count
    }

# ============================================================================
