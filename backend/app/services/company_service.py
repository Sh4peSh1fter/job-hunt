from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload # For eager loading if needed later
from typing import List, Optional

from app.models import Company as CompanyModel
from app.schemas import CompanyCreate, CompanyUpdate
from pydantic import HttpUrl # Import HttpUrl to check its type

async def create_company(db: AsyncSession, company_in: CompanyCreate) -> CompanyModel:
    """
    Creates a new company in the database.
    """
    company_data = company_in.model_dump()
    # Convert HttpUrl fields to strings before creating the SQLAlchemy model
    for field in ["website", "linkedin", "crunchbase", "glassdoor"]:
        if field in company_data and isinstance(company_data[field], HttpUrl):
            company_data[field] = str(company_data[field])

    db_company = CompanyModel(**company_data)
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company) # Refresh to get DB-generated values like ID, created_at
    return db_company

async def get_company_by_id(db: AsyncSession, company_id: int) -> Optional[CompanyModel]:
    """
    Retrieves a single company by its ID.
    """
    result = await db.execute(select(CompanyModel).filter(CompanyModel.id == company_id))
    return result.scalars().first()

async def get_companies(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[CompanyModel]:
    """
    Retrieves a list of companies with pagination.
    """
    result = await db.execute(select(CompanyModel).offset(skip).limit(limit))
    return result.scalars().all()

async def update_company(
    db: AsyncSession, company_id: int, company_in: CompanyUpdate
) -> Optional[CompanyModel]:
    """
    Updates an existing company in the database.
    """
    db_company = await get_company_by_id(db, company_id)
    if not db_company:
        return None

    update_data = company_in.model_dump(exclude_unset=True) # Get only fields that were actually set
    # Convert HttpUrl fields to strings before updating the SQLAlchemy model
    for field in ["website", "linkedin", "crunchbase", "glassdoor"]:
        if field in update_data and isinstance(update_data[field], HttpUrl):
            update_data[field] = str(update_data[field])

    for key, value in update_data.items():
        setattr(db_company, key, value)

    db.add(db_company) # Add the updated object to the session
    await db.commit()
    await db.refresh(db_company)
    return db_company

async def delete_company(db: AsyncSession, company_id: int) -> Optional[CompanyModel]:
    """
    Deletes a company from the database.
    Returns the deleted company object or None if not found.
    """
    db_company = await get_company_by_id(db, company_id)
    if not db_company:
        return None

    await db.delete(db_company)
    await db.commit()
    return db_company 