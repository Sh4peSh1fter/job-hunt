from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_db
from app.schemas.job_application import JobApplication, JobApplicationCreate, JobApplicationUpdate
from app.services import job_application_service

router = APIRouter(
    tags=["Job Applications"]
)

@router.post("/", response_model=JobApplication, status_code=201)
async def create_job_application(
    job_application_in: JobApplicationCreate,
    db: AsyncSession = Depends(get_async_db)
):
    # Basic validation: Ensure related company and job_source exist
    # This should ideally be more robust, perhaps checking in the service layer
    # or using foreign key constraints to let the DB handle it and catch exceptions.
    from app.services import company_service, job_source_service # Avoid circular imports at module level
    company = await company_service.get_company_by_id(db, job_application_in.company_id)
    if not company:
        raise HTTPException(status_code=404, detail=f"Company with id {job_application_in.company_id} not found")
    
    job_source = await job_source_service.get_job_source(db, job_application_in.discovered_through_id)
    if not job_source:
        raise HTTPException(status_code=404, detail=f"JobSource with id {job_application_in.discovered_through_id} not found")

    return await job_application_service.create_job_application(db=db, job_application_in=job_application_in)

@router.get("/", response_model=List[JobApplication])
async def read_job_applications(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    job_applications = await job_application_service.get_job_applications(db, skip=skip, limit=limit)
    print(f"DEBUG: In read_job_applications, found {len(job_applications)} applications.")
    return job_applications

@router.get("/{job_application_id}", response_model=JobApplication)
async def read_job_application(
    job_application_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    db_job_application = await job_application_service.get_job_application(db, job_application_id=job_application_id)
    if db_job_application is None:
        raise HTTPException(status_code=404, detail="JobApplication not found")
    return db_job_application

@router.put("/{job_application_id}", response_model=JobApplication)
async def update_job_application(
    job_application_id: int,
    job_application_in: JobApplicationUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    # Optional: Add validation for company_id and discovered_through_id if they are being updated
    if job_application_in.company_id is not None:
        from app.services import company_service
        company = await company_service.get_company(db, job_application_in.company_id)
        if not company:
            raise HTTPException(status_code=404, detail=f"Company with id {job_application_in.company_id} not found for update")
    
    if job_application_in.discovered_through_id is not None:
        from app.services import job_source_service
        job_source = await job_source_service.get_job_source(db, job_application_in.discovered_through_id)
        if not job_source:
            raise HTTPException(status_code=404, detail=f"JobSource with id {job_application_in.discovered_through_id} not found for update")

    updated_job_application = await job_application_service.update_job_application(
        db, job_application_id=job_application_id, job_application_in=job_application_in
    )
    if updated_job_application is None:
        raise HTTPException(status_code=404, detail="JobApplication not found")
    return updated_job_application

@router.delete("/{job_application_id}", response_model=JobApplication)
async def delete_job_application(
    job_application_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    deleted_job_application = await job_application_service.delete_job_application(db, job_application_id=job_application_id)
    if deleted_job_application is None:
        raise HTTPException(status_code=404, detail="JobApplication not found")
    return deleted_job_application 