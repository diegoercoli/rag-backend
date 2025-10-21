from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.knowledge_base import KnowledgeBase
from src.models.document import Document
from src.schemas.knowledge_base import (
    KnowledgeBaseCreate,
    KnowledgeBaseUpdate,
    KnowledgeBaseResponse,
    KnowledgeBaseCreateResponse,
    KnowledgeBaseWithDocumentsResponse
)
from src.schemas.document import DocumentResponse
from src.services.knowledgebase_service import KnowledgeBaseService

router = APIRouter()


@router.get("/", response_model=List[KnowledgeBaseResponse])
async def list_knowledge_bases(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """List all knowledge bases"""
    result = await db.execute(
        select(KnowledgeBase).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.post("/", response_model=KnowledgeBaseCreateResponse, status_code=201)
async def create_knowledge_base(
        kb: KnowledgeBaseCreate,
        db: AsyncSession = Depends(get_db)
):
    """
    Create or update a knowledge base, optionally with documents.

    Backend automatically sets:
    - created_at: Set to current datetime for new knowledge bases
    - updated_at: Set to current datetime when updating existing knowledge bases
    - version: Automatically incremented when document hash changes
    - obsolete: Automatically set to True for old versions
    - deleted: Automatically set to True for documents not in input

    Simple usage (knowledge base only):
        {
            "name": "Product Documentation"
        }

    Complex usage (with documents):
        {
            "name": "Product Documentation",
            "documents": [
                {
                    "filename": "user_guide.pdf",
                    "type": "pdf",
                    "hash": "a94a8fe5ccb19ba61c4c0873d391e987982fbbd3"
                }
            ]
        }
    """
    try:
        if not kb.documents:
            # Simple case: just create knowledge base
            result = await db.execute(
                select(KnowledgeBase).where(KnowledgeBase.name == kb.name)
            )
            existing_kb = result.scalar_one_or_none()

            if existing_kb:
                # Update existing knowledge base timestamp
                existing_kb.updated_at = datetime.utcnow()
                await db.commit()
                await db.refresh(existing_kb)

                return KnowledgeBaseCreateResponse(
                    id=existing_kb.id,
                    name=existing_kb.name,
                    created_at=existing_kb.created_at,
                    updated_at=existing_kb.updated_at
                )
            else:
                # Create new knowledge base
                db_kb = KnowledgeBase(
                    name=kb.name,
                    created_at=datetime.utcnow(),
                    updated_at=None
                )
                db.add(db_kb)
                await db.commit()
                await db.refresh(db_kb)

                return KnowledgeBaseCreateResponse(
                    id=db_kb.id,
                    name=db_kb.name,
                    created_at=db_kb.created_at,
                    updated_at=db_kb.updated_at
                )
        else:
            # Complex case: create knowledge base with documents
            documents_data = [
                {
                    'filename': doc.filename,
                    'type': doc.type,
                    'hash': doc.hash
                }
                for doc in kb.documents
            ]

            stats = await KnowledgeBaseService.process_knowledge_base_with_documents(
                db=db,
                kb_name=kb.name,
                documents_input=documents_data
            )

            # Commit the entire transaction
            await db.commit()

            # Fetch the created/updated knowledge base
            result = await db.execute(
                select(KnowledgeBase).where(KnowledgeBase.id == stats["knowledge_base_id"])
            )
            db_kb = result.scalar_one()

            return KnowledgeBaseCreateResponse(
                id=db_kb.id,
                name=db_kb.name,
                created_at=db_kb.created_at,
                updated_at=db_kb.updated_at,
                documents_added=stats["documents_added"],
                documents_updated=stats["documents_updated"],
                documents_marked_obsolete=stats["documents_marked_obsolete"],
                documents_marked_deleted=stats["documents_marked_deleted"]
            )
    except ValueError as ve:
        await db.rollback()
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        await db.rollback()
        import traceback
        print(f"Error creating knowledge base: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create knowledge base: {str(e)}"
        )


@router.get("/{kb_id}", response_model=KnowledgeBaseResponse)
async def get_knowledge_base(
        kb_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Get knowledge base by ID"""
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == kb_id)
    )
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    return kb


@router.patch("/{kb_id}", response_model=KnowledgeBaseResponse)
async def update_knowledge_base(
        kb_id: int,
        kb_update: KnowledgeBaseUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Update knowledge base"""
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == kb_id)
    )
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")

    for field, value in kb_update.dict(exclude_unset=True).items():
        setattr(kb, field, value)

    kb.updated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(kb)
    return kb


@router.delete("/{kb_id}", status_code=204)
async def delete_knowledge_base(
        kb_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Delete knowledge base"""
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == kb_id)
    )
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")

    await db.delete(kb)
    await db.commit()


@router.get("/{kb_id}/documents", response_model=KnowledgeBaseWithDocumentsResponse)
async def get_knowledge_base_with_documents(
        kb_id: int,
        not_obsolete: bool = True,
        db: AsyncSession = Depends(get_db)
):
    """
    Get knowledge base with its attributes and nested documents

    Parameters:
    - kb_id: Knowledge base ID
    - not_obsolete: If True (default), only returns documents where obsolete=False and deleted=False
    """
    # Get knowledge base
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == kb_id)
    )
    kb = result.scalar_one_or_none()
    if not kb:
        raise HTTPException(status_code=404, detail="Knowledge base not found")

    # Get documents with filter
    query = select(Document).where(Document.knowledge_base_id == kb_id)

    if not_obsolete:
        # Only show active documents (not obsolete and not deleted)
        query = query.where(Document.obsolete == False, Document.deleted == False)

    doc_result = await db.execute(query.order_by(Document.filename, Document.version.desc()))
    documents = doc_result.scalars().all()

    # Build response
    return KnowledgeBaseWithDocumentsResponse(
        id=kb.id,
        name=kb.name,
        created_at=kb.created_at,
        updated_at=kb.updated_at,
        documents=documents
    )

# ============================================================================