from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from app.models.enums import ApplicationEventTypeEnum

# Schema for common attributes
class ApplicationEventBase(BaseModel):
    job_application_id: int 
    event_type: ApplicationEventTypeEnum
    event_date: datetime = datetime.utcnow() # Default to now, can be overridden
    participants: Optional[str] = None
    notes: Optional[str] = None

# Schema for creating a new ApplicationEvent
class ApplicationEventCreate(ApplicationEventBase):
    pass

# Schema for updating an existing ApplicationEvent
class ApplicationEventUpdate(BaseModel):
    job_application_id: Optional[int] = None # Usually not changed, but possible
    event_type: Optional[ApplicationEventTypeEnum] = None
    event_date: Optional[datetime] = None
    participants: Optional[str] = None
    notes: Optional[str] = None

# Schema for reading/returning ApplicationEvent data
class ApplicationEvent(ApplicationEventBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    } 