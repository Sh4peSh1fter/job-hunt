from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.job_source import JobSource
from app.schemas.job_source import JobSourceCreate, JobSourceUpdate

async def get_job_source(db: AsyncSession, job_source_id: int) -> Optional[JobSource]:
    """
    Retrieves a single job source by its ID.

    Args:
        db: The AsyncSession for database interaction.
        job_source_id: The ID of the job source to retrieve.

    Returns:
        The JobSource object if found, otherwise None.
    """
    result = await db.execute(select(JobSource).filter(JobSource.id == job_source_id))
    return result.scalars().first()

async def get_job_source_by_name(db: AsyncSession, name: str) -> Optional[JobSource]:
    """
    Retrieves a single job source by its name.

    Args:
        db: The AsyncSession for database interaction.
        name: The name of the job source to retrieve.

    Returns:
        The JobSource object if found, otherwise None.
    """
    result = await db.execute(select(JobSource).filter(JobSource.name == name))
    return result.scalars().first()

async def get_job_sources(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[JobSource]:
    """
    Retrieves a list of job sources with pagination.

    Args:
        db: The AsyncSession for database interaction.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        A list of JobSource objects.
    """
    result = await db.execute(select(JobSource).offset(skip).limit(limit))
    return result.scalars().all()

async def create_job_source(db: AsyncSession, job_source_in: JobSourceCreate) -> JobSource:
    """
    Creates a new job source.

    Args:
        db: The AsyncSession for database interaction.
        job_source_in: The Pydantic schema containing data for the new job source.

    Returns:
        The newly created JobSource object.

    Raises:
        ValueError: If a job source with the same name already exists.
    """
    existing_source = await get_job_source_by_name(db, name=job_source_in.name)
    if existing_source:
        raise ValueError(f"JobSource with name '{job_source_in.name}' already exists.")

    # Convert Pydantic model to dict, ensuring HttpUrl is stringified
    create_data = job_source_in.model_dump()
    if 'website' in create_data and create_data['website'] is not None:
        create_data['website'] = str(create_data['website'])

    db_job_source = JobSource(**create_data)
    db.add(db_job_source)
    await db.commit()
    await db.refresh(db_job_source)
    return db_job_source

async def update_job_source(db: AsyncSession, job_source_id: int, job_source_in: JobSourceUpdate) -> Optional[JobSource]:
    """
    Updates an existing job source.

    Args:
        db: The AsyncSession for database interaction.
        job_source_id: The ID of the job source to update.
        job_source_in: The Pydantic schema containing updated data.

    Returns:
        The updated JobSource object if found and updated, otherwise None.

    Raises:
        ValueError: If updating the name conflicts with another existing job source.
    """
    db_job_source = await get_job_source(db, job_source_id=job_source_id)
    if not db_job_source:
        return None

    update_data = job_source_in.model_dump(exclude_unset=True)

    # If name is being updated, check for potential conflicts
    if "name" in update_data and update_data["name"] != db_job_source.name:
        name_to_check = update_data["name"]
        existing_source = await get_job_source_by_name(db, name=name_to_check)
        if existing_source and existing_source.id != job_source_id:
            raise ValueError(f"Another JobSource with name '{name_to_check}' already exists.")

    # Ensure HttpUrl is stringified if present in update_data
    if 'website' in update_data and update_data['website'] is not None:
        # Pydantic V2 HttpUrl might already be a string after model_dump if not exclude_none=True
        # but explicit conversion is safer if it's an HttpUrl object.
        if not isinstance(update_data['website'], str):
             update_data['website'] = str(update_data['website'])
    elif 'website' in update_data and update_data['website'] is None:
        # If website is explicitly set to None in the update, allow it
        pass 

    for key, value in update_data.items():
        setattr(db_job_source, key, value)
    
    await db.commit()
    await db.refresh(db_job_source)
    return db_job_source

async def delete_job_source(db: AsyncSession, job_source_id: int) -> Optional[JobSource]:
    """
    Deletes a job source by its ID.

    Args:
        db: The AsyncSession for database interaction.
        job_source_id: The ID of the job source to delete.

    Returns:
        The deleted JobSource object if found and deleted, otherwise None.
    
    Raises:
        ValueError: If the service layer has checks for related entities (e.g., JobApplications)
                    and finds that the JobSource is still in use (currently commented out).
    """
    db_job_source = await get_job_source(db, job_source_id)
    if db_job_source is None:
        return None
    
    # Add check for related JobApplications before deleting if strict referential integrity is desired at service level
    # from app.models.job_application import JobApplication
    # related_apps_query = await db.execute(select(JobApplication).filter(JobApplication.discovered_through_id == job_source_id).limit(1))
    # if related_apps_query.scalars().first():
    #     raise ValueError("Cannot delete JobSource: It is referenced by one or more JobApplications.")

    await db.delete(db_job_source)
    await db.commit()
    return db_job_source 