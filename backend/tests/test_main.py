import pytest
from httpx import AsyncClient, ASGITransport

from app.main import app # Import your FastAPI app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    json_response = response.json()
    assert json_response["api_status"] == "ok"
    assert json_response["db_status"] == "ok" 