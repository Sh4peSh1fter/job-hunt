from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware # Import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text # For executing a raw SQL query

from .db.database import get_async_db
from .routers import api_router # Import the main API router
# from .routers.job_applications import router as job_applications_router # <-- REVERTED
# from app.core.supabase_client import get_supabase_client # Example - remove if not used

app = FastAPI(
    title="Job Hunt API",
    description="API for the Job Hunt application, providing tools and data management.",
    version="0.1.0",
    # openapi_url="/api/v1/openapi.json",
    # docs_url="/api/v1/docs",
    # redoc_url="/api/v1/redoc"
)

# CORS Middleware Configuration
origins = [
    "http://localhost:3000",  # Allow your frontend origin
    # You can add other origins if needed, e.g., your deployed frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include the main API router with the /api/v1 prefix
app.include_router(api_router, prefix="/api/v1") # <-- REVERTED
# app.include_router(job_applications_router, prefix="/api/v1/job-applications") # <-- REVERTED

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_async_db)):
    """
    Performs a health check of the API and database connection.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        if result.scalar_one() == 1:
            db_status = "ok"
        else:
            db_status = "error: unexpected query result"
    except Exception as e:
        db_status = f"error: {str(e)}"

    return {"api_status": "ok", "db_status": db_status}

# Placeholder for future routers (tools, etc.)
# from .routers import items_router # Example
# app.include_router(items_router.router, prefix="/items", tags=["Items"])

if __name__ == "__main__":
    import uvicorn
    # This is for direct execution (e.g., python -m app.main)
    # For development, typically use: uvicorn app.main:app --reload --app-dir backend
    uvicorn.run(app, host="0.0.0.0", port=8000) 