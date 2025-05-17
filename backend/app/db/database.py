from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# Define the path to the SQLite database file.
# It will be created in the 'backend' directory, relative to the project root.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./job_hunt.db" # Stored in backend/job_hunt.db

async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# autocommit=False and autoflush=False are standard for FastAPI with SQLAlchemy.
# Commits should be handled explicitly in the service layer or endpoint after operations.
AsyncSessionLocal = sessionmaker(
    bind=async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

Base = declarative_base()

# Optional: A dependency to get a DB session in path operations
async def get_async_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Consider if auto-commit here is appropriate for your general use case.
            # For more control, commit within your route/service logic.
            # await session.commit() 
        except Exception:
            await session.rollback()
            raise
        # finally:
            # The 'async with' statement ensures the session is closed.
            # await session.close() 