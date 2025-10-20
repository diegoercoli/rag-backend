from datetime import date

from fastapi import APIRouter

from src.models.dataset import Dataset
from src.models.query import Query
from src.schemas.dataset import DatasetCreate, DatasetUpdate, DatasetResponse, DatasetCreateResponse
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.schemas.query import QueryResponse
from src.services.dataset_service import DatasetService

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


@router.post("/", response_model=DatasetCreateResponse, status_code=201)
async def create_dataset(
        dataset: DatasetCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Create or update a dataset, optionally with queries and ground truths.

    Backend automatically sets:
    - data_creation: Set to current date for new datasets
    - data_update: Set to current date when updating existing datasets

    Simple usage (dataset only):
        {
            "dataset_name": "my_dataset"
        }

    Complex usage (with queries and ground truths):
        {
            "dataset_name": "my_dataset",
            "queries": [
                {
                    "position_id": 1,
                    "prompt": "How do I...",
                    "device": "iPhone 14",
                    "customer": "premium_user",
                    "complexity": "Textual_Description",
                    "ground_truths": [
                        {
                            "filename": "manual.pdf",
                            "hierarchical_metadata": {
                                "id_section": "3.2.1",
                                "section_title": "Setup",
                                "depth": 3
                            },
                            "confidence": "High"
                        }
                    ]
                }
            ]
        }
    """
    try:
        if not dataset.queries:
            # Simple case: just create dataset
            db_dataset = Dataset(
                dataset_name=dataset.dataset_name,
                data_creation=date.today(),
                data_update=None
            )
            db.add(db_dataset)
            await db.commit()
            await db.refresh(db_dataset)

            return DatasetCreateResponse(
                id=db_dataset.id,
                dataset_name=db_dataset.dataset_name,
                data_creation=db_dataset.data_creation,
                data_update=db_dataset.data_update
            )
        else:
            # Complex case: create dataset with queries and ground truths
            stats = await DatasetService.process_dataset_with_queries(
                db=db,
                dataset_name=dataset.dataset_name,
                queries_input=dataset.queries
            )

            await db.commit()

            # Fetch the created/updated dataset
            result = await db.execute(
                select(Dataset).where(Dataset.id == stats["dataset_id"])
            )
            db_dataset = result.scalar_one()

            return DatasetCreateResponse(
                id=db_dataset.id,
                dataset_name=db_dataset.dataset_name,
                data_creation=db_dataset.data_creation,
                data_update=db_dataset.data_update,
                queries_added=stats["queries_added"],
                queries_updated=stats["queries_updated"],
                queries_marked_obsolete=stats["queries_marked_obsolete"],
                ground_truths_added=stats["ground_truths_added"]
            )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create dataset: {str(e)}"
        )


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
