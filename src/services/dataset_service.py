from datetime import date
from typing import List, Optional, Tuple, Dict, Set
from sqlalchemy import select, and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.dataset import Dataset
from src.models.query import Query
from src.models.ground_truth import GroundTruth
from src.models.hierarchical_metadata import HierarchicalMetadata
from src.models import ConfidenceLevel
from src.schemas.ground_truth import GroundTruthInput
from src.schemas.hierarchical_metadata import HierarchicalMetadataInput
from src.schemas.query import QueryInput


class DatasetService:
    """Service layer for dataset operations"""

    @staticmethod
    async def get_or_create_dataset(
            db: AsyncSession,
            dataset_name: str
    ) -> Tuple[Dataset, bool]:
        """Get existing dataset by name or create new one"""
        result = await db.execute(
            select(Dataset).where(Dataset.dataset_name == dataset_name)
        )
        existing_dataset = result.scalar_one_or_none()

        if existing_dataset:
            return existing_dataset, False

        new_dataset = Dataset(
            dataset_name=dataset_name,
            data_creation=date.today(),
            data_update=None
        )
        db.add(new_dataset)
        await db.flush()
        return new_dataset, True

    @staticmethod
    async def update_dataset_timestamp(db: AsyncSession, dataset: Dataset) -> None:
        """Update the dataset's data_update timestamp"""
        dataset.data_update = date.today()
        await db.flush()

    @staticmethod
    async def get_latest_query_version(
            db: AsyncSession,
            position_id: int,
            dataset_id: int
    ) -> Optional[Query]:
        """Get the latest (highest version) of a query at a specific position"""
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
        return result.scalar_one_or_none()

    @staticmethod
    async def get_next_version(
            db: AsyncSession,
            position_id: int,
            dataset_id: int
    ) -> int:
        """Get the next version number for a query"""
        result = await db.execute(
            select(func.max(Query.version))
            .where(
                and_(
                    Query.position_id == position_id,
                    Query.dataset_id == dataset_id
                )
            )
        )
        max_version = result.scalar()
        return (max_version or 0) + 1

    @staticmethod
    def _create_ground_truth_signature(
            filename: str,
            confidence: ConfidenceLevel,
            metadata_input: Optional[HierarchicalMetadataInput]
    ) -> str:
        """
        Create a unique signature for a ground truth for comparison purposes

        Args:
            filename: Ground truth filename
            confidence: Confidence level
            metadata_input: Hierarchical metadata input

        Returns:
            String signature representing the ground truth
        """
        if metadata_input:
            return f"{filename}|{confidence.value}|{metadata_input.id_section}|{metadata_input.section_title}|{metadata_input.depth}"
        return f"{filename}|{confidence.value}|None|None|None|None"

    @staticmethod
    def _create_ground_truth_signature_from_db(ground_truth: GroundTruth) -> str:
        """
        Create a unique signature for a ground truth from database object

        Args:
            ground_truth: GroundTruth database object

        Returns:
            String signature representing the ground truth
        """
        if ground_truth.hierarchical_metadata:
            hm = ground_truth.hierarchical_metadata
            return f"{ground_truth.filename}|{ground_truth.confidence.value}|{hm.id_section}|{hm.section_title}|{hm.depth}"
        return f"{ground_truth.filename}|{ground_truth.confidence.value}|None|None|None"

    @staticmethod
    async def has_ground_truths_changed(
            existing_query: Query,
            ground_truths_input: List[GroundTruthInput]
    ) -> bool:
        """
        Check if ground truths have changed

        Args:
            existing_query: Existing query from database (with ground_truths loaded)
            ground_truths_input: New ground truth input data

        Returns:
            True if ground truths changed, False otherwise
        """
        # Create signatures for existing ground truths
        existing_signatures: Set[str] = set()
        for gt in existing_query.ground_truths:
            signature = DatasetService._create_ground_truth_signature_from_db(gt)
            existing_signatures.add(signature)

        # Create signatures for new ground truths
        new_signatures: Set[str] = set()
        for gt_input in ground_truths_input:
            signature = DatasetService._create_ground_truth_signature(
                gt_input.filename,
                gt_input.confidence,
                gt_input.hierarchical_metadata
            )
            new_signatures.add(signature)

        # Compare sets - if they're different, ground truths have changed
        return existing_signatures != new_signatures

    @staticmethod
    async def has_query_changed(
            db: AsyncSession,
            existing_query: Query,
            query_input: QueryInput
    ) -> bool:
        """
        Check if query attributes or ground truths have changed

        Args:
            db: Database session
            existing_query: Existing query from database
            query_input: New query input data

        Returns:
            True if attributes or ground truths changed, False otherwise
        """
        # Check if basic attributes changed
        attributes_changed = (
                existing_query.prompt != query_input.prompt or
                existing_query.device != query_input.device or
                existing_query.customer != query_input.customer or
                existing_query.complexity.value != query_input.complexity.value
        )

        if attributes_changed:
            return True

        # Check if ground truths changed
        ground_truths_changed = await DatasetService.has_ground_truths_changed(
            existing_query,
            query_input.ground_truths
        )

        return ground_truths_changed

    @staticmethod
    async def create_or_find_ground_truth(
            db: AsyncSession,
            filename: str,
            confidence: ConfidenceLevel,
            metadata_id: Optional[int]
    ) -> GroundTruth:
        """Create or find existing ground truth by attributes"""
        result = await db.execute(
            select(GroundTruth).where(
                and_(
                    GroundTruth.filename == filename,
                    GroundTruth.confidence == confidence,
                    GroundTruth.hierarchical_metadata_id == metadata_id
                )
            )
        )
        existing_gt = result.scalar_one_or_none()

        if existing_gt:
            return existing_gt

        new_gt = GroundTruth(
            filename=filename,
            confidence=confidence,
            hierarchical_metadata_id=metadata_id
        )
        db.add(new_gt)
        await db.flush()
        return new_gt

    @staticmethod
    async def create_or_update_hierarchical_metadata(
            db: AsyncSession,
            metadata_input: Optional[HierarchicalMetadataInput]
    ) -> Optional[int]:
        """Create or find existing hierarchical metadata"""
        if not metadata_input:
            return None

        result = await db.execute(
            select(HierarchicalMetadata).where(
                and_(
                    HierarchicalMetadata.id_section == metadata_input.id_section,
                    HierarchicalMetadata.section_title == metadata_input.section_title,
                    HierarchicalMetadata.depth == metadata_input.depth,
                )
            )
        )
        existing_metadata = result.scalar_one_or_none()

        if existing_metadata:
            return existing_metadata.id

        new_metadata = HierarchicalMetadata(
            id_section=metadata_input.id_section,
            section_title=metadata_input.section_title,
            depth=metadata_input.depth,
        )
        db.add(new_metadata)
        await db.flush()
        return new_metadata.id

    @staticmethod
    async def associate_ground_truths_with_query(
            db: AsyncSession,
            query: Query,
            ground_truths_input: List[GroundTruthInput]
    ) -> int:
        """Associate ground truths with a query version"""
        count = 0
        for gt_input in ground_truths_input:
            metadata_id = await DatasetService.create_or_update_hierarchical_metadata(
                db, gt_input.hierarchical_metadata
            )

            ground_truth = await DatasetService.create_or_find_ground_truth(
                db,
                filename=gt_input.filename,
                confidence=gt_input.confidence,
                metadata_id=metadata_id
            )

            if ground_truth not in query.ground_truths:
                query.ground_truths.append(ground_truth)
                count += 1

        return count

    @staticmethod
    async def validate_query_ids(queries_input: List[QueryInput]) -> None:
        """Validate that position IDs are unique"""
        if not queries_input:
            return

        position_ids = [q.position_id for q in queries_input]

        if len(position_ids) != len(set(position_ids)):
            raise ValueError("Duplicate position IDs found in input")

    @staticmethod
    async def process_dataset_with_queries(
            db: AsyncSession,
            dataset_name: str,
            queries_input: List[QueryInput]
    ) -> Dict[str, int]:
        """Process dataset creation/update with queries and ground truths"""
        stats = {
            "dataset_id": 0,
            "queries_added": 0,
            "queries_updated": 0,
            "queries_marked_obsolete": 0,
            "ground_truths_added": 0
        }

        await DatasetService.validate_query_ids(queries_input)

        dataset, is_new = await DatasetService.get_or_create_dataset(db, dataset_name)
        stats["dataset_id"] = dataset.id

        dataset_modified = False

        for query_input in queries_input:
            # Get latest query version with ground truths eagerly loaded
            result = await db.execute(
                select(Query)
                .where(
                    and_(
                        Query.position_id == query_input.position_id,
                        Query.dataset_id == dataset.id
                    )
                )
                .order_by(Query.version.desc())
                .limit(1)
            )
            latest_query = result.scalar_one_or_none()

            if latest_query:
                # Eagerly load ground truths and their metadata for comparison
                await db.refresh(latest_query, ['ground_truths'])
                for gt in latest_query.ground_truths:
                    await db.refresh(gt, ['hierarchical_metadata'])

                # Check if query or ground truths changed
                if await DatasetService.has_query_changed(db, latest_query, query_input):
                    # Mark old version as obsolete
                    latest_query.obsolete = True
                    stats["queries_marked_obsolete"] += 1

                    # Create new version
                    next_version = await DatasetService.get_next_version(
                        db, query_input.position_id, dataset.id
                    )

                    new_query = Query(
                        position_id=query_input.position_id,
                        dataset_id=dataset.id,
                        version=next_version,
                        prompt=query_input.prompt,
                        device=query_input.device,
                        customer=query_input.customer,
                        complexity=query_input.complexity,
                        obsolete=False
                    )
                    db.add(new_query)
                    await db.flush()

                    gt_count = await DatasetService.associate_ground_truths_with_query(
                        db, new_query, query_input.ground_truths
                    )
                    stats["ground_truths_added"] += gt_count
                    stats["queries_updated"] += 1
                    dataset_modified = True
                else:
                    # Query and ground truths haven't changed - do nothing
                    pass
            else:
                # Create first version
                new_query = Query(
                    position_id=query_input.position_id,
                    dataset_id=dataset.id,
                    version=1,
                    prompt=query_input.prompt,
                    device=query_input.device,
                    customer=query_input.customer,
                    complexity=query_input.complexity,
                    obsolete=False
                )
                db.add(new_query)
                await db.flush()

                gt_count = await DatasetService.associate_ground_truths_with_query(
                    db, new_query, query_input.ground_truths
                )
                stats["ground_truths_added"] += gt_count
                stats["queries_added"] += 1
                dataset_modified = True

        if dataset_modified:
            await DatasetService.update_dataset_timestamp(db, dataset)

        return stats