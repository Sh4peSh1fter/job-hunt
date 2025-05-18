from fastapi import APIRouter

from . import companies
from . import job_applications
from . import job_sources

api_router = APIRouter() # Main router to include all sub-routers

api_router.include_router(companies.router, prefix="/companies", tags=["companies"])
api_router.include_router(job_applications.router, prefix="/job_applications", tags=["job_applications"])
api_router.include_router(job_sources.router, prefix="/job_sources", tags=["job_sources"])

# The main app will include this api_router with a /api/v1 prefix for all routes above.

# You could also include routers without the /api/v1 prefix if preferred, e.g.:
# api_router.include_router(companies.router)
# api_router.include_router(job_sources.router) 