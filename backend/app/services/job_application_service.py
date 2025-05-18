from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.models.job_application import JobApplication
from app.schemas.job_application import JobApplicationCreate, JobApplicationUpdate

async def get_job_application(db: AsyncSession, job_application_id: int) -> Optional[JobApplication]:
    """
    Retrieves a single job application by its ID.

    Args:
        db: The AsyncSession for database interaction.
        job_application_id: The ID of the job application to retrieve.

    Returns:
        The JobApplication object if found, otherwise None.
    """
    result = await db.execute(select(JobApplication).filter(JobApplication.id == job_application_id))
    return result.scalars().first()

async def get_job_applications(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[JobApplication]:
    """
    Retrieves a list of job applications with pagination.

    Args:
        db: The AsyncSession for database interaction.
        skip: Number of records to skip for pagination.
        limit: Maximum number of records to return.

    Returns:
        A list of JobApplication objects.
    """
    result = await db.execute(select(JobApplication).offset(skip).limit(limit))
    return result.scalars().all()

async def create_job_application(db: AsyncSession, job_application_in: JobApplicationCreate) -> JobApplication:
    """
    Creates a new job application.

    Args:
        db: The AsyncSession for database interaction.
        job_application_in: The Pydantic schema containing data for the new job application.

    Returns:
        The newly created JobApplication object.
    """
    # Convert Pydantic model to dict, ensuring HttpUrl is stringified
    create_data = job_application_in.model_dump()
    if 'job_url' in create_data and create_data['job_url'] is not None:
        create_data['job_url'] = str(create_data['job_url'])
    # Add similar conversions for other HttpUrl fields if they exist in JobApplicationCreate

    db_job_application = JobApplication(**create_data)
    db.add(db_job_application)
    await db.commit()
    await db.refresh(db_job_application)
    return db_job_application

async def update_job_application(db: AsyncSession, job_application_id: int, job_application_in: JobApplicationUpdate) -> Optional[JobApplication]:
    """
    Updates an existing job application.

    Args:
        db: The AsyncSession for database interaction.
        job_application_id: The ID of the job application to update.
        job_application_in: The Pydantic schema containing updated data.

    Returns:
        The updated JobApplication object if found and updated, otherwise None.
    """
    db_job_application = await get_job_application(db, job_application_id)
    if not db_job_application:
        return None

    update_data = job_application_in.model_dump(exclude_unset=True)

    # Ensure HttpUrl is stringified if present in update_data
    if 'job_url' in update_data and update_data['job_url'] is not None:
        if not isinstance(update_data['job_url'], str):
            update_data['job_url'] = str(update_data['job_url'])
    elif 'job_url' in update_data and update_data['job_url'] is None:
        pass # Allow explicit None
    # Add similar conversions for other HttpUrl fields if they exist in JobApplicationUpdate

    for key, value in update_data.items():
        setattr(db_job_application, key, value)
    
    await db.commit()
    await db.refresh(db_job_application)
    return db_job_application

async def delete_job_application(db: AsyncSession, job_application_id: int) -> Optional[JobApplication]:
    """
    Deletes a job application by its ID.

    Args:
        db: The AsyncSession for database interaction.
        job_application_id: The ID of the job application to delete.

    Returns:
        The deleted JobApplication object if found and deleted, otherwise None.
    """
    db_job_application = await get_job_application(db, job_application_id)
    if db_job_application is None:
        return None
    
    await db.delete(db_job_application)
    await db.commit()
    return db_job_application 