# This file makes the 'schemas' directory a Python package.
# Pydantic schemas for request/response validation will be defined here. 

from .company import Company, CompanyCreate, CompanyUpdate, CompanyBase
from .job_source import JobSource, JobSourceCreate, JobSourceUpdate, JobSourceBase
from .job_application import JobApplication, JobApplicationCreate, JobApplicationUpdate, JobApplicationBase
from .application_event import ApplicationEvent, ApplicationEventCreate, ApplicationEventUpdate, ApplicationEventBase

__all__ = [
    "Company", "CompanyCreate", "CompanyUpdate", "CompanyBase",
    "JobSource", "JobSourceCreate", "JobSourceUpdate", "JobSourceBase",
    "JobApplication", "JobApplicationCreate", "JobApplicationUpdate", "JobApplicationBase",
    "ApplicationEvent", "ApplicationEventCreate", "ApplicationEventUpdate", "ApplicationEventBase",
] 