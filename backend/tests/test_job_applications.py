import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession # For type hinting

from app.main import app # Your FastAPI app
from app.schemas import JobApplicationCreate, JobApplicationUpdate, JobApplication # Pydantic schemas
from app.schemas import CompanyCreate # For creating prerequisite company
from app.schemas import JobSourceCreate # For creating prerequisite job source
from app.models.enums import ApplicationStatusEnum, EmploymentTypeEnum

# We rely on the `client` fixture and `clear_data_before_each_test` fixture 
# from test_companies.py or a potential conftest.py for these tests.

@pytest.mark.asyncio
async def test_create_and_read_job_application(client: AsyncClient):
    # 1. Create a prerequisite Company
    company_data = {"name": "Test App Co", "industry": "Applications"}
    company_resp = await client.post("/api/v1/companies/", json=company_data)
    assert company_resp.status_code == 201, company_resp.text
    company_id = company_resp.json()["id"]

    # 2. Create a prerequisite JobSource
    source_data = {"name": "Test App Source", "type": "Job Board"}
    source_resp = await client.post("/api/v1/job_sources/", json=source_data)
    assert source_resp.status_code == 201, source_resp.text
    source_id = source_resp.json()["id"]

    # 3. Create JobApplication
    app_data = {
        "company_id": company_id,
        "title": "Software Engineer (Test)",
        "job_url": "https://testappco.example.com/job/swe123",
        "status": ApplicationStatusEnum.APPLIED.value, # Use .value for enums in JSON
        "discovered_through_id": source_id,
        "employment_type": EmploymentTypeEnum.FULL_TIME.value,
        "location_city": "Testville",
        "is_remote": False
    }
    response = await client.post("/api/v1/job_applications/", json=app_data)
    assert response.status_code == 201, response.text
    created_app_data = response.json()

    assert created_app_data["title"] == app_data["title"]
    assert created_app_data["company_id"] == company_id
    assert created_app_data["discovered_through_id"] == source_id
    assert created_app_data["status"] == app_data["status"]
    assert "id" in created_app_data
    app_id = created_app_data["id"]

    # Now try to read the application
    response_read = await client.get(f"/api/v1/job_applications/{app_id}")
    assert response_read.status_code == 200, response_read.text
    read_app_data = response_read.json()
    assert read_app_data["id"] == app_id
    assert read_app_data["title"] == app_data["title"]

@pytest.mark.asyncio
async def test_read_job_application_not_found(client: AsyncClient):
    non_existent_id = 999777
    response = await client.get(f"/api/v1/job_applications/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "JobApplication not found"

@pytest.mark.asyncio
async def test_create_job_application_company_not_found(client: AsyncClient):
    source_data = {"name": "Temp Source For App Test", "type": "Other"}
    source_resp = await client.post("/api/v1/job_sources/", json=source_data)
    assert source_resp.status_code == 201
    source_id = source_resp.json()["id"]

    app_data_bad_co = {
        "company_id": 99999, # Non-existent company
        "title": "Test Job Bad Co",
        "job_url": "https://example.com/job",
        "discovered_through_id": source_id
    }
    response = await client.post("/api/v1/job_applications/", json=app_data_bad_co)
    assert response.status_code == 404 # Based on router validation
    assert "Company with id 99999 not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_create_job_application_source_not_found(client: AsyncClient):
    company_data = {"name": "Temp Co For App Test"}
    company_resp = await client.post("/api/v1/companies/", json=company_data)
    assert company_resp.status_code == 201
    company_id = company_resp.json()["id"]

    app_data_bad_source = {
        "company_id": company_id,
        "title": "Test Job Bad Source",
        "job_url": "https://example.com/job2",
        "discovered_through_id": 88888 # Non-existent source
    }
    response = await client.post("/api/v1/job_applications/", json=app_data_bad_source)
    assert response.status_code == 404 # Based on router validation
    assert "JobSource with id 88888 not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_read_all_job_applications(client: AsyncClient):
    # Create prerequisites
    co1 = await client.post("/api/v1/companies/", json={"name": "App List Co 1"}); co1_id = co1.json()["id"]
    src1 = await client.post("/api/v1/job_sources/", json={"name": "App List Src 1", "type": "Recruiter"}); src1_id = src1.json()["id"]
    co2 = await client.post("/api/v1/companies/", json={"name": "App List Co 2"}); co2_id = co2.json()["id"]
    src2 = await client.post("/api/v1/job_sources/", json={"name": "App List Src 2", "type": "Networking"}); src2_id = src2.json()["id"]

    app_data1 = {"company_id": co1_id, "title": "App Lister 1", "job_url": "https://ex1.com", "discovered_through_id": src1_id}
    app_data2 = {"company_id": co2_id, "title": "App Lister 2", "job_url": "https://ex2.com", "discovered_through_id": src2_id}
    
    await client.post("/api/v1/job_applications/", json=app_data1)
    await client.post("/api/v1/job_applications/", json=app_data2)

    response = await client.get("/api/v1/job_applications/")
    assert response.status_code == 200
    apps_list = response.json()
    assert isinstance(apps_list, list)
    assert len(apps_list) == 2 # Because clear_data_before_each_test runs
    
    titles = [app["title"] for app in apps_list]
    assert app_data1["title"] in titles
    assert app_data2["title"] in titles

@pytest.mark.asyncio
async def test_update_job_application(client: AsyncClient):
    co = await client.post("/api/v1/companies/", json={"name": "Update App Co"}); co_id = co.json()["id"]
    src = await client.post("/api/v1/job_sources/", json={"name": "Update App Src", "type": "Job Board"}); src_id = src.json()["id"]

    app_data = {"company_id": co_id, "title": "Updateable App", "job_url": "https://upd8.com", "discovered_through_id": src_id, "status": ApplicationStatusEnum.APPLIED.value}
    create_response = await client.post("/api/v1/job_applications/", json=app_data)
    assert create_response.status_code == 201, create_response.text
    app_id = create_response.json()["id"]

    update_payload = {"title": "Super Updated App", "status": ApplicationStatusEnum.OFFERED.value, "notes": None}
    update_response = await client.put(f"/api/v1/job_applications/{app_id}", json=update_payload)
    assert update_response.status_code == 200, update_response.text
    updated_app_data = update_response.json()

    assert updated_app_data["id"] == app_id
    assert updated_app_data["title"] == update_payload["title"]
    assert updated_app_data["status"] == update_payload["status"]
    assert updated_app_data["notes"] == update_payload["notes"]

@pytest.mark.asyncio
async def test_update_job_application_not_found(client: AsyncClient):
    non_existent_id = 666777
    update_payload = {"title": "Ghost App Update"}
    response = await client.put(f"/api/v1/job_applications/{non_existent_id}", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "JobApplication not found"

@pytest.mark.asyncio
async def test_delete_job_application(client: AsyncClient):
    co = await client.post("/api/v1/companies/", json={"name": "Delete App Co"}); co_id = co.json()["id"]
    src = await client.post("/api/v1/job_sources/", json={"name": "Delete App Src", "type": "Other"}); src_id = src.json()["id"]
    
    app_data = {"company_id": co_id, "title": "Deletable App", "job_url": "https://del.com", "discovered_through_id": src_id}
    create_response = await client.post("/api/v1/job_applications/", json=app_data)
    assert create_response.status_code == 201
    app_id = create_response.json()["id"]

    delete_response = await client.delete(f"/api/v1/job_applications/{app_id}")
    assert delete_response.status_code == 200, delete_response.text
    deleted_data = delete_response.json()
    assert deleted_data["id"] == app_id
    assert deleted_data["title"] == app_data["title"]

    # Verify it's actually deleted
    get_response = await client.get(f"/api/v1/job_applications/{app_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_job_application_not_found(client: AsyncClient):
    non_existent_id = 555777
    response = await client.delete(f"/api/v1/job_applications/{non_existent_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "JobApplication not found" 