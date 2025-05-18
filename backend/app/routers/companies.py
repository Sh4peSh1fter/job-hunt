from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_async_db
from app.schemas import Company, CompanyCreate, CompanyUpdate # Pydantic schemas for Company
from app.services import company_service # Our new service

router = APIRouter(
    tags=["Companies"]    # Tag for API documentation (e.g., Swagger UI)
)

@router.post("/", response_model=Company, status_code=status.HTTP_201_CREATED)
async def create_new_company(
    company_in: CompanyCreate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Create a new company.
    """
    # The service function returns the SQLAlchemy model instance.
    # FastAPI will automatically convert it to the `Company` Pydantic response_model.
    return await company_service.create_company(db=db, company_in=company_in)

@router.get("/", response_model=List[Company])
async def read_all_companies(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Retrieve all companies with pagination.
    """
    companies = await company_service.get_companies(db=db, skip=skip, limit=limit)
    return companies

@router.get("/{company_id}", response_model=Company)
async def read_company_by_id(
    company_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Retrieve a single company by its ID.
    """
    db_company = await company_service.get_company_by_id(db=db, company_id=company_id)
    if db_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return db_company

@router.put("/{company_id}", response_model=Company)
async def update_existing_company(
    company_id: int,
    company_in: CompanyUpdate,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Update an existing company.
    """
    updated_company = await company_service.update_company(
        db=db, company_id=company_id, company_in=company_in
    )
    if updated_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return updated_company

@router.delete("/{company_id}", response_model=Company)
async def remove_company(
    company_id: int,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Delete a company by its ID.
    """
    deleted_company = await company_service.delete_company(db=db, company_id=company_id)
    if deleted_company is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    # Optionally, you could return a 204 No Content on successful deletion
    # with no response body, but returning the deleted object can be useful.
    return deleted_company 