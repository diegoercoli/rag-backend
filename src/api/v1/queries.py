from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.query import Query
from src.schemas.query import QueryCreate, QueryUpdate, QueryResponse

router = APIRouter()

@router.get("/", response_model=List[QueryResponse])
async def list_queries(
    skip: int = 0,
    limit: int = 100,
    dataset_id: Optional[int] = None,
    obsolete: Optional[bool] = None,
    db: AsyncSession = Depends(get_db)
):
    """List queries with filters"""
    query = select(Query)
    
    if dataset_id is not None:
        query = query.where(Query.dataset_id == dataset_id)
    if obsolete is not None:
        query = query.where(Query.obsolete == obsolete)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=QueryResponse, status_code=201)
async def create_query(
    query_data: QueryCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new query"""
    db_query = Query(**query_data.dict())
    db.add(db_query)
    await db.commit()
    await db.refresh(db_query)
    return db_query

@router.get("/{query_id}", response_model=QueryResponse)
async def get_query(
    query_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get query by ID"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    return query

@router.patch("/{query_id}", response_model=QueryResponse)
async def update_query(
    query_id: int,
    query_update: QueryUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update query"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    for field, value in query_update.dict(exclude_unset=True).items():
        setattr(query, field, value)
    
    await db.commit()
    await db.refresh(query)
    return query

@router.delete("/{query_id}", status_code=204)
async def delete_query(
    query_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete query"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail="Query not found")
    
    await db.delete(query)
    await db.commit()

# ============================================================================
