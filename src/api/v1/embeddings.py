from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.models.embedding import Embedding
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse
from src.schemas.embedding import EmbeddingResponse, EmbeddingCreate, EmbeddingUpdate

router = APIRouter()

@router.get("/", response_model=List[EmbeddingResponse])
async def list_embeddings(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all embedding models"""
    result = await db.execute(
        select(Embedding).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=EmbeddingResponse, status_code=201)
async def create_embedding(
    embedding: EmbeddingCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create embedding model"""
    db_embedding = Embedding(**embedding.dict())
    db.add(db_embedding)
    await db.commit()
    await db.refresh(db_embedding)
    return db_embedding

@router.get("/{embedding_id}", response_model=EmbeddingResponse)
async def get_embedding(
    embedding_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get embedding by ID"""
    result = await db.execute(
        select(Embedding).where(Embedding.id == embedding_id)
    )
    embedding = result.scalar_one_or_none()
    if not embedding:
        raise HTTPException(status_code=404, detail="Embedding not found")
    return embedding

@router.delete("/{embedding_id}", status_code=204)
async def delete_embedding(
    embedding_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete embedding"""
    result = await db.execute(
        select(Embedding).where(Embedding.id == embedding_id)
    )
    embedding = result.scalar_one_or_none()
    if not embedding:
        raise HTTPException(status_code=404, detail="Embedding not found")
    
    await db.delete(embedding)
    await db.commit()

@router.patch("/{embedding_id}", response_model=EmbeddingResponse)
async def update_embedding(
    embedding_id: int = Path(..., gt=0),
    embedding_update: EmbeddingUpdate = ...,
    db: AsyncSession = Depends(get_db)
):
    """Update embedding by ID"""
    result = await db.execute(
        select(Embedding).where(Embedding.id == embedding_id)
    )
    embedding = result.scalar_one_or_none()
    if not embedding:
        raise HTTPException(status_code=404, detail="Embedding not found")

    for field, value in embedding_update.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(embedding, field, value)

    await db.commit()
    await db.refresh(embedding)
    return embedding

# ============================================================================
