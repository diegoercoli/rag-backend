from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse

router = APIRouter()

@router.get("/", response_model=List[ConfigurationResponse])
async def list_configurations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """List all configurations"""
    result = await db.execute(
        select(Configuration).offset(skip).limit(limit)
    )
    return result.scalars().all()

@router.post("/", response_model=ConfigurationResponse, status_code=201)
async def create_configuration(
    config: ConfigurationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new configuration"""
    db_config = Configuration(**config.dict())
    db.add(db_config)
    await db.commit()
    await db.refresh(db_config)
    return db_config

@router.get("/{config_id}", response_model=ConfigurationResponse)
async def get_configuration(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get configuration by ID"""
    result = await db.execute(
        select(Configuration).where(Configuration.id == config_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    return config

@router.delete("/{config_id}", status_code=204)
async def delete_configuration(
    config_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete configuration"""
    result = await db.execute(
        select(Configuration).where(Configuration.id == config_id)
    )
    config = result.scalar_one_or_none()
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    await db.delete(config)
    await db.commit()

# ============================================================================
