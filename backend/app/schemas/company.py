from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime

from app.models.enums import CompanyPhaseEnum
# We might need JobApplication schemas here later if we want to return them nested

# Schema for common attributes
class CompanyBase(BaseModel):
    name: str
    foundation_date: Optional[datetime] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    phase: Optional[CompanyPhaseEnum] = None
    website: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    crunchbase: Optional[HttpUrl] = None
    glassdoor: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    notes: Optional[str] = None
    related_articles: Optional[str] = None # Storing as string (comma-separated URLs)

# Schema for creating a new Company
class CompanyCreate(CompanyBase):
    pass

# Schema for updating an existing Company (all fields optional)
class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    foundation_date: Optional[datetime] = None
    industry: Optional[str] = None
    size: Optional[str] = None
    phase: Optional[CompanyPhaseEnum] = None
    website: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    crunchbase: Optional[HttpUrl] = None
    glassdoor: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    notes: Optional[str] = None
    related_articles: Optional[str] = None

# Schema for reading/returning Company data from the API
# Forward declaration for JobApplication schema to handle circular dependencies if needed later
# class JobApplication(BaseModel): ... 

class Company(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # job_applications: List[JobApplication] = [] # Example if returning related applications

    model_config = {
        "from_attributes": True
    } 