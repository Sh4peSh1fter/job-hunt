from fastapi import APIRouter

# Explicitly import the 'router' object from each sub-module
from .companies import router as companies_router
from .job_applications import router as job_applications_router
from .job_sources import router as job_sources_router
# If you add more routers, follow this pattern:
# from .application_events import router as application_events_router 

api_router = APIRouter() # Main router to include all sub-routers

# Include the imported routers
api_router.include_router(companies_router, prefix="/companies", tags=["companies"])
api_router.include_router(job_applications_router, prefix="/job-apps", tags=["job_applications"])
api_router.include_router(job_sources_router, prefix="/job-srcs", tags=["job_sources"])
# api_router.include_router(application_events_router, prefix="/application_events", tags=["application_events"])

# The main app will include this api_router with a /api/v1 prefix for all routes above.

# You could also include routers without the /api/v1 prefix if preferred, e.g.:
# api_router.include_router(companies.router)
# api_router.include_router(job_sources.router) 