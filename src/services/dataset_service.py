# Business logic for dataset management
from datetime import date
from typing import List, Optional, Tuple, Dict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.dataset import Dataset
from src.models.query import Query
from src.models.ground_truth import GroundTruth
from src.models.hierarchical_metadata import HierarchicalMetadata
from src.schemas.dataset_queries import (
    DatasetInput, QueryInput, GroundTruthInput,
    HierarchicalMetadataInput
)


class DatasetService:
    """Service layer for dataset operations"""

    @staticmethod
    async def get_or_create_dataset(
            db: AsyncSession,
            dataset_input: DatasetInput
    ) -> Tuple[Dataset, bool]:
        """
        Get existing dataset by name or create new one

        Args:
            db: Database session
            dataset_input: Dataset input data

        Returns:
            Tuple of (Dataset object, is_new boolean)
        """
        # Check if dataset exists
        result = await db.execute(
            select(Dataset).where(Dataset.dataset_name == dataset_input.dataset_name)
        )
        existing_dataset = result.scalar_one_or_none()

        if existing_dataset:
            # Update dataset if data_update is provided
            if dataset_input.data_update:
                existing_dataset.data_update = dataset_input.data_update
                await db.flush()
            return existing_dataset, False

        # Create new dataset
        new_dataset = Dataset(
            dataset_name=dataset_input.dataset_name,
            data_creation=dataset_input.data_creation or date.today(),
            data_update=dataset_input.data_update
        )
        db.add(new_dataset)
        await db.flush()  # Flush to get the ID
        return new_dataset, True

    @staticmethod
    async def find_matching_query(
            db: AsyncSession,
            dataset_id: int,
            query_input: QueryInput
    ) -> Optional[Query]:
        """
        Find existing query that matches the input query

        Args:
            db: Database session
            dataset_id: Dataset ID to search within
            query_input: Query input data

        Returns:
            Matching Query object or None
        """
        result = await db.execute(
            select(Query).where(
                Query.dataset_id == dataset_id,
                Query.prompt == query_input.prompt,
                Query.obsolete == False  # Only match non-obsolete queries
            )
        )
        return result.scalar_one_or_none()

    @staticmethod
    def has_query_changed(existing_query: Query, query_input: QueryInput) -> bool:
        """
        Check if query attributes have changed

        Args:
            existing_query: Existing query from database
            query_input: New query input data

        Returns:
            True if attributes changed, False otherwise
        """
        return (
                existing_query.device != query_input.device or
                existing_query.customer != query_input.customer or
                existing_query.complexity.value != query_input.complexity.value
        )

    @staticmethod
    async def create_or_update_hierarchical_metadata(
            db: AsyncSession,
            metadata_input: Optional[HierarchicalMetadataInput]
    ) -> Optional[int]:
        """
        Create or find existing hierarchical metadata

        Args:
            db: Database session
            metadata_input: Metadata input data

        Returns:
            Hierarchical metadata ID or None
        """
        if not metadata_input:
            return None

        # Try to find existing metadata with same attributes
        result = await db.execute(
            select(HierarchicalMetadata).where(
                HierarchicalMetadata.id_section == metadata_input.id_section,
                HierarchicalMetadata.section_title == metadata_input.section_title,
                HierarchicalMetadata.depth == metadata_input.depth,
            )
        )
        existing_metadata = result.scalar_one_or_none()

        if existing_metadata:
            return existing_metadata.id

        # Create new metadata
        new_metadata = HierarchicalMetadata(
            id_section=metadata_input.id_section,
            section_title=metadata_input.section_title,
            depth=metadata_input.depth,
        )
        db.add(new_metadata)
        await db.flush()
        return new_metadata.id

    @staticmethod
    async def create_ground_truths(
            db: AsyncSession,
            query_id: int,
            ground_truths: List[GroundTruthInput]
    ) -> int:
        """
        Create ground truth entries for a query

        Args:
            db: Database session
            query_id: Query ID to associate ground truths with
            ground_truths: List of ground truth input data

        Returns:
            Number of ground truths created
        """
        count = 0
        for gt_input in ground_truths:
            # Create or get hierarchical metadata
            metadata_id = await DatasetService.create_or_update_hierarchical_metadata(
                db, gt_input.hierarchical_metadata
            )

            # Create ground truth
            ground_truth = GroundTruth(
                filename=gt_input.filename,
                query_id=query_id,
                hierarchical_metadata_id=metadata_id,
                confidence=gt_input.confidence
            )
            db.add(ground_truth)
            count += 1

        return count

    @staticmethod
    async def process_bulk_dataset(
            db: AsyncSession,
            dataset_input: DatasetInput,
            queries_input: List[QueryInput]
    ) -> Dict[str, int]:
        """
        Process bulk dataset creation/update with queries and ground truths

        Args:
            db: Database session
            dataset_input: Dataset input data
            queries_input: List of query input data

        Returns:
            Dictionary with statistics about the operation
        """
        stats = {
            "dataset_id": 0,
            "queries_added": 0,
            "queries_updated": 0,
            "queries_marked_obsolete": 0,
            "ground_truths_added": 0
        }

        # Get or create dataset
        dataset, is_new = await DatasetService.get_or_create_dataset(db, dataset_input)
        stats["dataset_id"] = dataset.id

        # Process each query
        for query_input in queries_input:
            # Check if query already exists
            existing_query = await DatasetService.find_matching_query(
                db, dataset.id, query_input
            )

            if existing_query:
                # Check if attributes changed
                if DatasetService.has_query_changed(existing_query, query_input):
                    # Mark existing query as obsolete
                    existing_query.obsolete = True
                    stats["queries_marked_obsolete"] += 1

                    # Create new query with updated attributes
                    new_query = Query(
                        prompt=query_input.prompt,
                        device=query_input.device,
                        customer=query_input.customer,
                        complexity=query_input.complexity,
                        obsolete=False,
                        dataset_id=dataset.id
                    )
                    db.add(new_query)
                    await db.flush()

                    # Create ground truths for new query
                    gt_count = await DatasetService.create_ground_truths(
                        db, new_query.id, query_input.ground_truths
                    )
                    stats["ground_truths_added"] += gt_count
                    stats["queries_updated"] += 1
                else:
                    # Query hasn't changed, just add any new ground truths
                    gt_count = await DatasetService.create_ground_truths(
                        db, existing_query.id, query_input.ground_truths
                    )
                    stats["ground_truths_added"] += gt_count
            else:
                # Create new query
                new_query = Query(
                    prompt=query_input.prompt,
                    device=query_input.device,
                    customer=query_input.customer,
                    complexity=query_input.complexity,
                    obsolete=query_input.obsolete,
                    dataset_id=dataset.id
                )
                db.add(new_query)
                await db.flush()

                # Create ground truths
                gt_count = await DatasetService.create_ground_truths(
                    db, new_query.id, query_input.ground_truths
                )
                stats["ground_truths_added"] += gt_count
                stats["queries_added"] += 1

        return stats