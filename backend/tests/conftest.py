import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator

from app.main import app # Your FastAPI app
from app.db.database import Base, get_async_db # Import Base and get_async_db

# Define the in-memory SQLite URL for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# Create a new async engine for testing
test_async_engine = create_async_engine(
    TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a new sessionmaker for testing
TestAsyncSessionLocal = sessionmaker(
    bind=test_async_engine, class_=AsyncSession, autocommit=False, autoflush=False
)

# Fixture to set up and tear down the database for the entire test session
@pytest.fixture(scope="session", autouse=True)
async def setup_test_database():
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Dependency override for get_async_db to use the test database
async def override_get_async_db() -> AsyncGenerator[AsyncSession, None]:
    async with TestAsyncSessionLocal() as session:
        yield session

# Apply the dependency override to the app for testing
# This needs to be done when the app is loaded, so it's often done here
# or in a way that ensures it's applied before any test client is created.
app.dependency_overrides[get_async_db] = override_get_async_db

# Fixture to provide an AsyncClient instance per test function
@pytest.fixture(scope="function")
async def client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
        yield ac

@pytest.fixture(scope="function", autouse=True)
async def clear_data_before_each_test(client: AsyncClient): # Added client fixture dependency to ensure override is active
    """Clears all data from tables before each test function runs."""
    # Ensures that the dependency override for get_async_db is active before clearing data.
    # The client fixture itself ensures the app is set up with the override.
    async with TestAsyncSessionLocal() as session: 
        async with session.begin(): 
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
        await session.commit() 