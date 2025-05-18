from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime, date # Ensure date is imported

from app.models.enums import EmploymentTypeEnum, ApplicationStatusEnum
# We might need ApplicationEvent schemas here later

# Schema for common attributes
class JobApplicationBase(BaseModel):
    company_id: int
    title: str
    description_text: Optional[str] = None
    job_url: HttpUrl
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    is_remote: Optional[bool] = False
    employment_type: Optional[EmploymentTypeEnum] = None
    used_resume: Optional[str] = None
    cover_letter_file_path: Optional[str] = None
    requested_salary_min: Optional[int] = None
    requested_salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    date_posted: Optional[date] = None # Changed to date type
    status: ApplicationStatusEnum = ApplicationStatusEnum.CONSIDERING
    discovered_through_id: int
    applied_through_text: Optional[str] = None 
    referral: Optional[str] = None
    notes: Optional[str] = None

# Schema for creating a new JobApplication
class JobApplicationCreate(JobApplicationBase):
    pass

# Schema for updating an existing JobApplication
class JobApplicationUpdate(BaseModel):
    company_id: Optional[int] = None
    title: Optional[str] = None
    description_text: Optional[str] = None
    job_url: Optional[HttpUrl] = None
    location_city: Optional[str] = None
    location_country: Optional[str] = None
    is_remote: Optional[bool] = None
    employment_type: Optional[EmploymentTypeEnum] = None
    used_resume: Optional[str] = None
    cover_letter_file_path: Optional[str] = None
    requested_salary_min: Optional[int] = None
    requested_salary_max: Optional[int] = None
    salary_currency: Optional[str] = None
    date_posted: Optional[date] = None
    status: Optional[ApplicationStatusEnum] = None
    discovered_through_id: Optional[int] = None
    applied_through_text: Optional[str] = None
    referral: Optional[str] = None
    notes: Optional[str] = None

# Schema for reading/returning JobApplication data
# Forward declaration for ApplicationEvent schema if needed for nesting
# class ApplicationEvent(BaseModel): ...

class JobApplication(JobApplicationBase):
    id: int
    created_at: datetime
    updated_at: datetime
    # events: List[ApplicationEvent] = [] # Example if returning related events

    model_config = {
        "from_attributes": True
    } 