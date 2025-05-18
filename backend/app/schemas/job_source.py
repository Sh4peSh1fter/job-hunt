from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime

from app.models.enums import JobSourceTypeEnum # Assuming enums.py is in app.models

# Schema for common attributes
class JobSourceBase(BaseModel):
    name: str
    type: Optional[JobSourceTypeEnum] = None
    website: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    notes: Optional[str] = None

# Schema for creating a new JobSource
class JobSourceCreate(JobSourceBase):
    pass

# Schema for updating an existing JobSource (all fields optional)
class JobSourceUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[JobSourceTypeEnum] = None
    website: Optional[HttpUrl] = None
    short_description: Optional[str] = None
    notes: Optional[str] = None

# Schema for reading/returning JobSource data from the API
class JobSource(JobSourceBase): # In Pydantic v2, this is often just JobSource(JobSourceBase) or similar
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True # Replaces orm_mode = True in Pydantic v1
    } 