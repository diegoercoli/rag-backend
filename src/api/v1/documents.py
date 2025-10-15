from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.configuration import Configuration
from src.models.document import Document
from src.schemas.configuration import ConfigurationCreate, ConfigurationResponse
from src.schemas.document import DocumentResponse, DocumentCreate

router = APIRouter()

@router.get("/", response_model=List[DocumentResponse])
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List documents"""
    query = select(Document)
    if type:
        query = query.where(Document.type == type)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    document: DocumentCreate,
    db: AsyncSession = Depends(get_db)
):
    """Upload a new document"""
    db_document = Document(**document.dict())
    db.add(db_document)
    await db.commit()
    await db.refresh(db_document)
    return db_document

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get document by ID"""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete document"""
    result = await db.execute(
        select(Document).where(Document.id == document_id)
    )
    document = result.scalar_one_or_none()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await db.delete(document)
    await db.commit()

@router.get("/check-hash/{hash}")
async def check_document_hash(
    hash: str,
    db: AsyncSession = Depends(get_db)
):
    """Check if document exists by hash"""
    result = await db.execute(
        select(Document).where(Document.hash == hash)
    )
    document = result.scalar_one_or_none()
    return {"exists": document is not None, "document": document}

# ============================================================================
