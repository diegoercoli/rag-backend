from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, and_
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
        latest_only: bool = True,
        db: AsyncSession = Depends(get_db)
):
    """List queries with filters"""
    query = select(Query)

    if dataset_id is not None:
        query = query.where(Query.dataset_id == dataset_id)
    if obsolete is not None:
        query = query.where(Query.obsolete == obsolete)
    if latest_only:
        query = query.where(Query.obsolete == False)

    query = query.offset(skip).limit(limit).order_by(
        Query.dataset_id, Query.position_id, Query.version.desc()
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=QueryResponse, status_code=201)
async def create_query(
        query_data: QueryCreate,
        db: AsyncSession = Depends(get_db)
):
    """Create a new query version"""
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
    """Get query by ID (auto-increment ID)"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail=f"Query {query_id} not found")
    return query


@router.get("/dataset/{dataset_id}/position/{position_id}", response_model=List[QueryResponse])
async def get_query_versions_by_position(
        dataset_id: int,
        position_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get all versions of a query at a specific position"""
    result = await db.execute(
        select(Query)
        .where(
            and_(
                Query.position_id == position_id,
                Query.dataset_id == dataset_id
            )
        )
        .order_by(Query.version.desc())
    )
    queries = result.scalars().all()
    if not queries:
        raise HTTPException(
            status_code=404,
            detail=f"No queries found at position {position_id} in dataset {dataset_id}"
        )
    return queries


@router.get("/dataset/{dataset_id}/position/{position_id}/latest", response_model=QueryResponse)
async def get_latest_query_at_position(
        dataset_id: int,
        position_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get the latest version of a query at a specific position"""
    result = await db.execute(
        select(Query)
        .where(
            and_(
                Query.position_id == position_id,
                Query.dataset_id == dataset_id
            )
        )
        .order_by(Query.version.desc())
        .limit(1)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(
            status_code=404,
            detail=f"No query found at position {position_id} in dataset {dataset_id}"
        )
    return query


@router.patch("/{query_id}", response_model=QueryResponse)
async def update_query(
        query_id: int,
        query_update: QueryUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update a query by ID"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail=f"Query {query_id} not found")

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
    """Delete a query by ID"""
    result = await db.execute(
        select(Query).where(Query.id == query_id)
    )
    query = result.scalar_one_or_none()
    if not query:
        raise HTTPException(status_code=404, detail=f"Query {query_id} not found")

    await db.delete(query)
    await db.commit()

# ============================================================================