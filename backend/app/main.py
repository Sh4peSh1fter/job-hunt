from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text # For executing a raw SQL query

from .db.database import get_async_db #, settings # If settings were needed here
# from .config import settings # If you need app settings from config.py

app = FastAPI(
    title="Job Hunt API",
    description="API for the Job Hunt application, providing tools and data management.",
    version="0.1.0"
)

@app.get("/health", tags=["Health"])
async def health_check(db: AsyncSession = Depends(get_async_db)):
    """
    Performs a health check of the API and database connection.
    """
    try:
        # Try to execute a simple query to check DB connection
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