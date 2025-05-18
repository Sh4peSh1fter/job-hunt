import pytest
from httpx import AsyncClient
# sqlalchemy imports for type hinting in test functions might still be useful if directly using AsyncSession, else remove
# from sqlalchemy.ext.asyncio import AsyncSession 
# from sqlalchemy.orm import sessionmaker # No longer needed here
# from typing import Dict, Any, AsyncGenerator # No longer needed for override_get_async_db

# app, schemas, Base, get_async_db are imported by conftest or used by fixtures there, 
# but direct schema imports are needed for test data definition.
from app.schemas import CompanyCreate, CompanyUpdate, Company 

# All fixtures (TEST_SQLALCHEMY_DATABASE_URL, test_async_engine, TestAsyncSessionLocal,
# setup_test_database, override_get_async_db, app.dependency_overrides, client, clear_data_before_each_test)
# are now expected to be in conftest.py

# Helper function to create a company directly via service for setup (optional)
# async def create_company_directly(db: AsyncSession, company_data: Dict[str, Any]):
#     from app.services import company_service
#     company_schema = CompanyCreate(**company_data)
#     return await company_service.create_company(db=db, company_in=company_schema)

@pytest.mark.asyncio
async def test_create_and_read_company(client: AsyncClient):
    company_data = {
        "name": "Test Company Inc.",
        "industry": "Software",
        "website": "https://testcompany.example.com",
        "short_description": "A test software company."
    }
    response = await client.post("/api/v1/companies/", json=company_data)
    assert response.status_code == 201
    created_company_data = response.json()

    assert created_company_data["name"] == company_data["name"]
    assert created_company_data["industry"] == company_data["industry"]
    assert str(created_company_data["website"]).rstrip('/') == company_data["website"].rstrip('/')
    assert created_company_data["short_description"] == company_data["short_description"]
    assert "id" in created_company_data
    company_id = created_company_data["id"]

    # Now try to read the company
    response_read = await client.get(f"/api/v1/companies/{company_id}")
    assert response_read.status_code == 200
    read_company_data = response_read.json()
    assert read_company_data["id"] == company_id
    assert read_company_data["name"] == company_data["name"]

@pytest.mark.asyncio
async def test_read_company_not_found(client: AsyncClient):
    non_existent_id = 999999
    response = await client.get(f"/api/v1/companies/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

@pytest.mark.asyncio
async def test_read_all_companies(client: AsyncClient):
    # Create a couple of companies to ensure there's data
    company_data1 = {"name": "List Test Corp 1", "industry": "Testing"}
    company_data2 = {"name": "List Test Corp 2", "website": "https://list2.example.com"}
    # Attempt to create, but be mindful these might exist if tests run multiple times without DB reset
    # A better approach would be to ensure a clean DB or use truly unique names (e.g., UUIDs)
    # With the new setup, the DB is clean for each session, so direct creation is fine.
    await client.post("/api/v1/companies/", json=company_data1)
    await client.post("/api/v1/companies/", json=company_data2)

    response = await client.get("/api/v1/companies/")
    assert response.status_code == 200
    companies_list = response.json()
    assert isinstance(companies_list, list)
    # Now we can assert the exact length because the DB is clean per session/test.
    assert len(companies_list) == 2
    
    # Basic check for names
    names = [c["name"] for c in companies_list]
    assert company_data1["name"] in names
    assert company_data2["name"] in names

@pytest.mark.asyncio
async def test_update_company(client: AsyncClient):
    company_data = {"name": "Update Me Ltd.", "industry": "Initial"}
    create_response = await client.post("/api/v1/companies/", json=company_data)
    assert create_response.status_code == 201
    created_company = create_response.json()
    company_id = created_company["id"]

    update_payload = {"name": "Updated Name Co.", "industry": "Technology", "notes": "Updated notes."}
    update_response = await client.put(f"/api/v1/companies/{company_id}", json=update_payload)
    assert update_response.status_code == 200
    updated_company_data = update_response.json()

    assert updated_company_data["id"] == company_id
    assert updated_company_data["name"] == update_payload["name"]
    assert updated_company_data["industry"] == update_payload["industry"]
    # assert updated_company_data["notes"] == update_payload["notes"]

@pytest.mark.asyncio
async def test_update_company_not_found(client: AsyncClient):
    non_existent_id = 888888
    update_payload = {"name": "Ghost Update"}
    response = await client.put(f"/api/v1/companies/{non_existent_id}", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

@pytest.mark.asyncio
async def test_delete_company(client: AsyncClient):
    company_data = {"name": "Delete Me Corp.", "short_description": "Temporary"}
    create_response = await client.post("/api/v1/companies/", json=company_data)
    assert create_response.status_code == 201
    company_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/companies/{company_id}")
    assert delete_response.status_code == 200
    deleted_data = delete_response.json()
    assert deleted_data["id"] == company_id
    assert deleted_data["name"] == company_data["name"]

    # Verify it's actually deleted by trying to GET it
    get_response = await client.get(f"/api/v1/companies/{company_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_company_not_found(client: AsyncClient):
    non_existent_id = 777777
    response = await client.delete(f"/api/v1/companies/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Company not found"

# We will add more tests for list, update, and delete here.