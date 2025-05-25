# Job Applications API

**Base Path:** `/api/v1/job-apps` (Note: uses `/job-apps` prefix due to routing conflict resolution)

This API provides CRUD operations for job application entities.

## Schemas

-   **Request (Create):** `JobApplicationCreate` (see [Job Application Data Model](../data-models/job-application-model.md))
-   **Request (Update):** `JobApplicationUpdate` (see [Job Application Data Model](../data-models/job-application-model.md))
-   **Response:** `JobApplication` (see [Job Application Data Model](../data-models/job-application-model.md))

---

## Endpoints

### 1. Create a New Job Application

-   **Method:** `POST`
-   **Path:** `/`
-   **Description:** Creates a new job application record. It performs basic validation to ensure the related `company_id` and `discovered_through_id` (Job Source) exist.
-   **Request Body:** `JobApplicationCreate` schema.
-   **Response:** `201 Created` - Returns the created `JobApplication` object.
-   **Example `curl`:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/job-apps/" \
         -H "Content-Type: application/json" \
         -d '{
              "company_id": 1,
              "title": "Software Engineer",
              "job_url": "https://jobs.example.com/se123",
              "status": "Applied",
              "discovered_through_id": 1,
              "date_posted": "2024-05-20"
            }'
    ```

### 2. Read All Job Applications

-   **Method:** `GET`
-   **Path:** `/`
-   **Description:** Retrieves a list of all job applications, with optional pagination.
-   **Query Parameters:**
    -   `skip` (int, optional, default: 0): Number of records to skip.
    -   `limit` (int, optional, default: 100): Maximum number of records to return.
-   **Response:** `200 OK` - Returns a list of `JobApplication` objects.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/job-apps/?skip=0&limit=10"
    ```

### 3. Read Job Application by ID

-   **Method:** `GET`
-   **Path:** `/{job_application_id}`
-   **Description:** Retrieves a single job application by its unique ID.
-   **Path Parameters:**
    -   `job_application_id` (int, required): The ID of the job application to retrieve.
-   **Response:**
    -   `200 OK` - Returns the `JobApplication` object.
    -   `404 Not Found` - If the job application with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/job-apps/1"
    ```

### 4. Update an Existing Job Application

-   **Method:** `PUT`
-   **Path:** `/{job_application_id}`
-   **Description:** Updates an existing job application. It performs basic validation if `company_id` or `discovered_through_id` are being updated.
-   **Path Parameters:**
    -   `job_application_id` (int, required): The ID of the job application to update.
-   **Request Body:** `JobApplicationUpdate` schema. All fields are optional.
-   **Response:**
    -   `200 OK` - Returns the updated `JobApplication` object.
    -   `404 Not Found` - If the job application or related entities (if updated) do not exist.
-   **Example `curl`:**
    ```bash
    curl -X PUT "http://localhost:8000/api/v1/job-apps/1" \
         -H "Content-Type: application/json" \
         -d '{
              "status": "Interviewing",
              "notes": "Scheduled first interview."
            }'
    ```

### 5. Delete a Job Application

-   **Method:** `DELETE`
-   **Path:** `/{job_application_id}`
-   **Description:** Deletes a job application by its ID.
-   **Path Parameters:**
    -   `job_application_id` (int, required): The ID of the job application to delete.
-   **Response:**
    -   `200 OK` - Returns the deleted `JobApplication` object.
    -   `404 Not Found` - If the job application with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X DELETE "http://localhost:8000/api/v1/job-apps/1"
    ```

---

See also: [Job Application Data Model](../data-models/job-application-model.md) 