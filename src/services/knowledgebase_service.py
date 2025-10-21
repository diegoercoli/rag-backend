from datetime import datetime
from typing import List, Optional, Tuple, Dict, Set
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.knowledge_base import KnowledgeBase
from src.models.document import Document


class KnowledgeBaseService:
    """Service layer for knowledge base operations"""

    @staticmethod
    async def get_or_create_knowledge_base(
            db: AsyncSession,
            kb_name: str
    ) -> Tuple[KnowledgeBase, bool]:
        """Get existing knowledge base by name or create new one"""
        result = await db.execute(
            select(KnowledgeBase).where(KnowledgeBase.name == kb_name)
        )
        existing_kb = result.scalar_one_or_none()

        if existing_kb:
            return existing_kb, False

        new_kb = KnowledgeBase(name=kb_name)
        db.add(new_kb)
        await db.flush()
        return new_kb, True

    @staticmethod
    async def update_knowledge_base_timestamp(db: AsyncSession, kb: KnowledgeBase) -> None:
        """Update the knowledge base's updated_at timestamp"""
        kb.updated_at = datetime.utcnow()
        await db.flush()

    @staticmethod
    async def get_latest_document_version(
            db: AsyncSession,
            filename: str,
            kb_id: int
    ) -> Optional[Document]:
        """Get the latest (highest version) of a document by filename"""
        result = await db.execute(
            select(Document)
            .where(
                and_(
                    Document.filename == filename,
                    Document.knowledge_base_id == kb_id,
                    Document.obsolete == False,
                    Document.deleted == False
                )
            )
            .order_by(Document.version.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_next_version(
            db: AsyncSession,
            filename: str,
            kb_id: int
    ) -> float:
        """Get the next version number for a document"""
        result = await db.execute(
            select(func.max(Document.version))
            .where(
                and_(
                    Document.filename == filename,
                    Document.knowledge_base_id == kb_id
                )
            )
        )
        max_version = result.scalar()
        return (max_version or 0) + 1

    @staticmethod
    def _create_document_signature(filename: str, doc_type: str, doc_hash: str) -> str:
        """Create a unique signature for a document for comparison"""
        return f"{filename}|{doc_type}|{doc_hash}"

    @staticmethod
    async def get_active_documents(
            db: AsyncSession,
            kb_id: int
    ) -> List[Document]:
        """Get all active (not obsolete, not deleted) documents in knowledge base"""
        result = await db.execute(
            select(Document)
            .where(
                and_(
                    Document.knowledge_base_id == kb_id,
                    Document.obsolete == False,
                    Document.deleted == False
                )
            )
        )
        return result.scalars().all()

    @staticmethod
    async def mark_missing_documents_as_deleted(
            db: AsyncSession,
            kb_id: int,
            input_filenames: Set[str]
    ) -> int:
        """Mark documents not present in input as deleted"""
        active_docs = await KnowledgeBaseService.get_active_documents(db, kb_id)
        count = 0

        for doc in active_docs:
            if doc.filename not in input_filenames:
                doc.deleted = True
                count += 1

        await db.flush()
        return count

    @staticmethod
    async def process_knowledge_base_with_documents(
            db: AsyncSession,
            kb_name: str,
            documents_input: List[Dict]
    ) -> Dict[str, int]:
        """Process knowledge base creation/update with documents"""
        stats = {
            "knowledge_base_id": 0,
            "documents_added": 0,
            "documents_updated": 0,
            "documents_marked_obsolete": 0,
            "documents_marked_deleted": 0
        }

        kb, is_new = await KnowledgeBaseService.get_or_create_knowledge_base(db, kb_name)
        stats["knowledge_base_id"] = kb.id

        kb_modified = False
        input_filenames = {doc['filename'] for doc in documents_input}

        for doc_input in documents_input:
            filename = doc_input['filename']
            doc_type = doc_input['type']
            doc_hash = doc_input['hash']

            # Get latest active version of this document
            latest_doc = await KnowledgeBaseService.get_latest_document_version(
                db, filename, kb.id
            )

            if latest_doc:
                # Document exists - check if hash changed
                if latest_doc.hash != doc_hash:
                    # Hash changed - mark old version as obsolete
                    latest_doc.obsolete = True
                    stats["documents_marked_obsolete"] += 1

                    # Create new version
                    next_version = await KnowledgeBaseService.get_next_version(
                        db, filename, kb.id
                    )

                    new_doc = Document(
                        filename=filename,
                        version=next_version,
                        type=doc_type,
                        hash=doc_hash,
                        knowledge_base_id=kb.id,
                        obsolete=False,
                        deleted=False,
                        created_at=datetime.utcnow(),
                        updated_at=None
                    )
                    db.add(new_doc)
                    stats["documents_updated"] += 1
                    kb_modified = True
                else:
                    # Hash unchanged - do nothing
                    pass
            else:
                # New document - create first version
                new_doc = Document(
                    filename=filename,
                    version=1.0,
                    type=doc_type,
                    hash=doc_hash,
                    knowledge_base_id=kb.id,
                    obsolete=False,
                    deleted=False,
                    created_at=datetime.utcnow(),
                    updated_at=None
                )
                db.add(new_doc)
                stats["documents_added"] += 1
                kb_modified = True

        # Mark documents not in input as deleted
        if not is_new:
            deleted_count = await KnowledgeBaseService.mark_missing_documents_as_deleted(
                db, kb.id, input_filenames
            )
            stats["documents_marked_deleted"] = deleted_count
            if deleted_count > 0:
                kb_modified = True

        if kb_modified:
            await KnowledgeBaseService.update_knowledge_base_timestamp(db, kb)

        await db.flush()
        return stats