from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.chunk import Chunk
from src.models.chunking import Chunking
from src.schemas.chunk import ChunkResponse
from src.schemas.chunking import ChunkingCreate, ChunkingResponse

router = APIRouter()

@router.get("/", response_model=List[ChunkResponse])
async def list_chunks(
    filename: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List chunks"""
    query = select(Chunk)
    if filename:
        query = query.where(Chunk.filename.ilike(f"%{filename}%"))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{chunk_id}", response_model=ChunkResponse)
async def get_chunk(
    chunk_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get chunk details"""
    result = await db.execute(
        select(Chunk).where(Chunk.id == chunk_id)
    )
    chunk = result.scalar_one_or_none()
    if not chunk:
        raise HTTPException(status_code=404, detail="Chunk not found")
    return chunk
