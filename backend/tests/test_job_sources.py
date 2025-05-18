import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession # For type hinting
from typing import Dict, Any # For type hinting

# Assuming your main app and other fixtures are set up similarly to test_companies.py
# If not, these imports and fixtures might need adjustment.
from app.main import app # Your FastAPI app
from app.schemas import JobSourceCreate, JobSourceUpdate, JobSource # Pydantic schemas
from app.db.database import Base, get_async_db # Re-import if necessary for context, though overridden

# Test-specific DB setup is usually handled by conftest.py or shared fixtures
# For now, assuming the setup from test_companies.py (override_get_async_db, client fixture) is available globally
# or we can redefine minimal necessary parts here or move them to conftest.py.

# We rely on the `client` fixture and `clear_data_before_each_test` fixture 
# from test_companies.py or a potential conftest.py for these tests.

@pytest.mark.asyncio
async def test_create_and_read_job_source(client: AsyncClient):
    source_data = {
        "name": "Test Source Platform",
        "type": "Job Board", # Changed from "JOB_BOARD"
        "website": "https://testsource.example.com",
        "short_description": "A job board for testing."
    }
    response = await client.post("/api/v1/job_sources/", json=source_data)
    assert response.status_code == 201, response.text
    created_source_data = response.json()

    assert created_source_data["name"] == source_data["name"]
    assert created_source_data["type"] == source_data["type"]
    assert str(created_source_data["website"]).rstrip('/') == source_data["website"].rstrip('/')
    assert created_source_data["short_description"] == source_data["short_description"]
    assert "id" in created_source_data
    source_id = created_source_data["id"]

    # Now try to read the source
    response_read = await client.get(f"/api/v1/job_sources/{source_id}")
    assert response_read.status_code == 200, response_read.text
    read_source_data = response_read.json()
    assert read_source_data["id"] == source_id
    assert read_source_data["name"] == source_data["name"]

@pytest.mark.asyncio
async def test_create_job_source_duplicate_name(client: AsyncClient):
    source_data = {"name": "Unique Source Name", "type": "Company Website"} # Changed from "COMPANY_WEBSITE"
    response1 = await client.post("/api/v1/job_sources/", json=source_data)
    assert response1.status_code == 201, response1.text

    response2 = await client.post("/api/v1/job_sources/", json=source_data)
    assert response2.status_code == 400, response2.text # Expecting bad request due to duplicate name
    assert "already exists" in response2.json()["detail"]

@pytest.mark.asyncio
async def test_read_job_source_not_found(client: AsyncClient):
    non_existent_id = 999888
    response = await client.get(f"/api/v1/job_sources/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "JobSource not found"

@pytest.mark.asyncio
async def test_read_all_job_sources(client: AsyncClient):
    # Ensure a clean slate or known state due to clear_data_before_each_test
    source_data1 = {"name": "Source List Test 1", "type": "Referral Program"} # Changed from "REFERRAL"
    source_data2 = {"name": "Source List Test 2", "type": "Other", "website": "https://list2.example.com"} # Added type
    
    await client.post("/api/v1/job_sources/", json=source_data1)
    await client.post("/api/v1/job_sources/", json=source_data2)

    response = await client.get("/api/v1/job_sources/")
    assert response.status_code == 200
    sources_list = response.json()
    assert isinstance(sources_list, list)
    assert len(sources_list) == 2 # Because clear_data_before_each_test runs
    
    names = [s["name"] for s in sources_list]
    assert source_data1["name"] in names
    assert source_data2["name"] in names

@pytest.mark.asyncio
async def test_update_job_source(client: AsyncClient):
    source_data = {"name": "Updateable Source", "type": "Other"} # Changed from "OTHER"
    create_response = await client.post("/api/v1/job_sources/", json=source_data)
    assert create_response.status_code == 201
    created_source = create_response.json()
    source_id = created_source["id"]

    update_payload = {"name": "Updated Source Name", "notes": "Updated notes here."}
    update_response = await client.put(f"/api/v1/job_sources/{source_id}", json=update_payload)
    assert update_response.status_code == 200, update_response.text
    updated_source_data = update_response.json()

    assert updated_source_data["id"] == source_id
    assert updated_source_data["name"] == update_payload["name"]
    assert updated_source_data["notes"] == update_payload["notes"]
    assert updated_source_data["type"] == source_data["type"] # Original type should persist

@pytest.mark.asyncio
async def test_update_job_source_to_duplicate_name(client: AsyncClient):
    source1_data = {"name": "Source One For Update Test"}
    source2_data = {"name": "Source Two For Update Test"}
    await client.post("/api/v1/job_sources/", json=source1_data)
    resp2 = await client.post("/api/v1/job_sources/", json=source2_data)
    source2_id = resp2.json()["id"]

    update_payload_conflict = {"name": "Source One For Update Test"} # Conflicts with source1
    response = await client.put(f"/api/v1/job_sources/{source2_id}", json=update_payload_conflict)
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"]

@pytest.mark.asyncio
async def test_update_job_source_not_found(client: AsyncClient):
    non_existent_id = 777888
    update_payload = {"name": "Ghost Source Update"}
    response = await client.put(f"/api/v1/job_sources/{non_existent_id}", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "JobSource not found"

@pytest.mark.asyncio
async def test_delete_job_source(client: AsyncClient):
    source_data = {"name": "Deletable Source", "short_description": "Will be deleted."}
    create_response = await client.post("/api/v1/job_sources/", json=source_data)
    assert create_response.status_code == 201
    source_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/job_sources/{source_id}")
    assert delete_response.status_code == 200, delete_response.text
    deleted_data = delete_response.json()
    assert deleted_data["id"] == source_id
    assert deleted_data["name"] == source_data["name"]

    # Verify it's actually deleted
    get_response = await client.get(f"/api/v1/job_sources/{source_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_job_source_not_found(client: AsyncClient):
    non_existent_id = 666888
    response = await client.delete(f"/api/v1/job_sources/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "JobSource not found"

@pytest.mark.asyncio
async def test_update_job_source_name_conflict(client: AsyncClient):
    initial_name = "Original Source for Conflict Test"
    conflicting_name = "Existing Source Name for Conflict"

    # Create the source that will cause a conflict
    await client.post("/api/v1/job_sources/", json={"name": conflicting_name, "type": "Networking"})

    # Create the source to be updated
    response_create = await client.post("/api/v1/job_sources/", json={"name": initial_name, "type": "Job Board"})
    assert response_create.status_code == 201
    source_to_update_id = response_create.json()["id"]

    # Attempt to update to the conflicting name
    update_payload = {"name": conflicting_name}
    response_update = await client.put(f"/api/v1/job_sources/{source_to_update_id}", json=update_payload)
    assert response_update.status_code == 400
    assert "already exists" in response_update.json()["detail"] 