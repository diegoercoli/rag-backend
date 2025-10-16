from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.blacklist import BlacklistChapter
from src.models.configuration import Configuration
from src.schemas.blacklist import (
    BlacklistChapterCreate, BlacklistChapterResponse, BlacklistEntryCreate
)

router = APIRouter()

# Blacklist Chapter endpoints
@router.get("/chapters", response_model=List[BlacklistChapterResponse])
async def list_blacklist_chapters(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all blacklist chapters"""
    result = await db.execute(
        select(BlacklistChapter).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/chapters", response_model=BlacklistChapterResponse, status_code=201)
async def create_blacklist_chapter(
    chapter: BlacklistChapterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create blacklist chapter"""
    db_chapter = BlacklistChapter(**chapter.model_dump())
    db.add(db_chapter)
    await db.commit()
    await db.refresh(db_chapter)
    return db_chapter

@router.get("/chapters/{chapter_id}", response_model=BlacklistChapterResponse)
async def get_blacklist_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get chapter details"""
    result = await db.execute(
        select(BlacklistChapter).where(BlacklistChapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter

@router.put("/chapters/{chapter_id}", response_model=BlacklistChapterResponse)
async def update_blacklist_chapter(
    chapter_id: int,
    chapter_update: BlacklistChapterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Update chapter"""
    result = await db.execute(
        select(BlacklistChapter).where(BlacklistChapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    chapter.name = chapter_update.name
    await db.commit()
    await db.refresh(chapter)
    return chapter

@router.delete("/chapters/{chapter_id}", status_code=204)
async def delete_blacklist_chapter(
    chapter_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete chapter"""
    result = await db.execute(
        select(BlacklistChapter).where(BlacklistChapter.id == chapter_id)
    )
    chapter = result.scalar_one_or_none()
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    
    await db.delete(chapter)
    await db.commit()


