from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from src.database import get_db
import src.models
from src.models.experiment import Experiment
from src.schemas.experiment import ExperimentCreate, ExperimentUpdate, ExperimentResponse

router = APIRouter()

@router.get("/", response_model=List[ExperimentResponse])
async def list_experiments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000),
    configuration_id: Optional[int] = None,
    dataset_id: Optional[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """List experiments with optional filters"""
    query = select(Experiment)
    
    if configuration_id:
        query = query.where(Experiment.configuration_id == configuration_id)
    if dataset_id:
        query = query.where(Experiment.dataset_id == dataset_id)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=ExperimentResponse, status_code=201)
async def create_experiment(
    experiment: ExperimentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new experiment"""
    db_experiment = Experiment(**experiment.dict())
    db.add(db_experiment)
    await db.commit()
    await db.refresh(db_experiment)
    return db_experiment

@router.get("/{experiment_id}", response_model=ExperimentResponse)
async def get_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get experiment by ID"""
    result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return experiment

@router.patch("/{experiment_id}", response_model=ExperimentResponse)
async def update_experiment(
    experiment_id: int,
    experiment_update: ExperimentUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update experiment timing data"""
    result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    for field, value in experiment_update.dict(exclude_unset=True).items():
        setattr(experiment, field, value)
    
    await db.commit()
    await db.refresh(experiment)
    return experiment

@router.delete("/{experiment_id}", status_code=204)
async def delete_experiment(
    experiment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete experiment"""
    result = await db.execute(
        select(Experiment).where(Experiment.id == experiment_id)
    )
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    
    await db.delete(experiment)
    await db.commit()

# ============================================================================
