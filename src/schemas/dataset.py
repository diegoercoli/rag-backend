from datetime import date
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

from datetime import date
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class DatasetBase(BaseModel):
    """
    Base schema containing common fields shared across dataset operations.

    This base class defines the core attributes of a dataset that are used
    across multiple Pydantic schemas (create, update, response). Following
    the DRY (Don't Repeat Yourself) principle, common fields are defined
    here and inherited by other dataset schemas.

    Attributes:
        dataset_name: Unique identifier name for the dataset. Must be provided
            for all operations that include this base schema.
        data_creation: The date when the dataset was originally created.
            This is a required field that establishes the dataset's inception.
        data_update: Optional date indicating when the dataset was last updated.
            Defaults to None if the dataset has never been updated.

    Note:
        This class is not used directly in API endpoints but serves as a
        parent class for other dataset schemas.
    """
    dataset_name: str
    data_creation: date
    data_update: Optional[date] = None


class DatasetCreate(DatasetBase):
    """
    Schema for creating a new dataset via API requests.

    This schema is used to validate incoming data when a client sends a POST
    request to create a new dataset. It inherits all fields from DatasetBase,
    ensuring that all required dataset information is provided during creation.

    Usage:
        Used as a request body model in FastAPI POST endpoints:

        @router.post("/datasets", response_model=DatasetResponse)
        def create_dataset(dataset: DatasetCreate, db: Session = Depends(get_db)):
            # dataset is automatically validated against this schema
            ...

    Validation:
        - dataset_name: Required, must be a non-empty string
        - data_creation: Required, must be a valid date
        - data_update: Optional, must be a valid date if provided

    Example:
        {
            "dataset_name": "customer_feedback_2024",
            "data_creation": "2024-01-15",
            "data_update": null
        }
    """
    pass


class DatasetUpdate(BaseModel):
    """
    Schema for updating an existing dataset via API requests.

    This schema is used to validate incoming data when a client sends a PATCH
    or PUT request to update an existing dataset. It intentionally includes
    only fields that can be modified after creation.

    Design Decisions:
        - Does NOT inherit from DatasetBase because we don't want to allow
          updating dataset_name or data_creation (immutable fields)
        - All fields are optional to support partial updates
        - Typically used with exclude_unset=True to only update provided fields

    Usage:
        Used as a request body model in FastAPI PATCH/PUT endpoints:

        @router.patch("/datasets/{id}", response_model=DatasetResponse)
        def update_dataset(id: int, dataset: DatasetUpdate, db: Session = ...):
            update_data = dataset.model_dump(exclude_unset=True)
            # Only updates fields that were actually provided
            ...

    Attributes:
        data_update: Optional date indicating when the dataset was last updated.
            This is the only field that can be modified after dataset creation.

    Example:
        {
            "data_update": "2024-10-15"
        }
    """
    data_update: Optional[date] = None


class DatasetResponse(DatasetBase):
    """
    Schema for serializing dataset data in API responses.

    This schema is used when sending dataset information back to API clients
    in response to GET, POST, or PUT requests. It extends DatasetBase with
    database-generated fields that should be included in responses but not
    in create requests.

    Usage:
        Used as a response_model in FastAPI endpoints:

        @router.get("/datasets/{id}", response_model=DatasetResponse)
        def get_dataset(id: int, db: Session = Depends(get_db)):
            dataset = db.query(Dataset).filter(Dataset.id == id).first()
            return dataset  # Automatically converted to DatasetResponse

    Attributes:
        id: Database-generated primary key for the dataset. This field is
            added to the base fields and is populated by the database.

        (Inherited from DatasetBase):
        dataset_name: The unique name of the dataset
        data_creation: When the dataset was created
        data_update: When the dataset was last updated (if applicable)

    Configuration:
        from_attributes = True: Enables automatic conversion from SQLAlchemy
            ORM models to Pydantic models. Without this, you'd need to manually
            convert ORM objects to dictionaries before returning them.

    Example Response:
        {
            "id": 42,
            "dataset_name": "customer_feedback_2024",
            "data_creation": "2024-01-15",
            "data_update": "2024-10-15"
        }
    """
    id: int

    class Config:
        """
        Pydantic configuration for DatasetResponse.

        from_attributes: Allows the model to be populated from SQLAlchemy ORM
            objects by reading their attributes. Previously known as orm_mode
            in Pydantic v1. This enables seamless conversion between database
            models and API response models.
        """
        from_attributes = True

# ============================================================================
