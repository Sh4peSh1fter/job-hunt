from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_db
from app.schemas.job_source import JobSource, JobSourceCreate, JobSourceUpdate
from app.services import job_source_service

router = APIRouter()

@router.post("/", response_model=JobSource, status_code=201)
async def create_job_source(
    job_source_in: JobSourceCreate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        return await job_source_service.create_job_source(db=db, job_source_in=job_source_in)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{job_source_id}", response_model=JobSource)
async def read_job_source(
    job_source_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    db_job_source = await job_source_service.get_job_source(db, job_source_id=job_source_id)
    if db_job_source is None:
        raise HTTPException(status_code=404, detail="JobSource not found")
    return db_job_source

@router.get("/", response_model=List[JobSource])
async def read_job_sources(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    job_sources = await job_source_service.get_job_sources(db, skip=skip, limit=limit)
    return job_sources

@router.put("/{job_source_id}", response_model=JobSource)
async def update_job_source(
    job_source_id: int,
    job_source_in: JobSourceUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    try:
        updated_job_source = await job_source_service.update_job_source(
            db, job_source_id=job_source_id, job_source_in=job_source_in
        )
        if updated_job_source is None:
            raise HTTPException(status_code=404, detail="JobSource not found")
        return updated_job_source
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete("/{job_source_id}", response_model=JobSource)
async def delete_job_source(
    job_source_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    # If the service layer raises ValueError on deletion due to FK constraints:
    try:
        deleted_job_source = await job_source_service.delete_job_source(db, job_source_id=job_source_id)
        if deleted_job_source is None:
            raise HTTPException(status_code=404, detail="JobSource not found")
        return deleted_job_source
    except ValueError as e: # Catches error if delete is blocked by service layer due to relations
        raise HTTPException(status_code=400, detail=str(e)) 