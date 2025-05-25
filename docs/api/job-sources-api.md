# Job Sources API

**Base Path:** `/api/v1/job-srcs` (Note: uses `/job-srcs` prefix due to routing conflict resolution)

This API provides CRUD operations for job source entities.

## Schemas

-   **Request (Create):** `JobSourceCreate` (see [Job Source Data Model](../data-models/job-source-model.md))
-   **Request (Update):** `JobSourceUpdate` (see [Job Source Data Model](../data-models/job-source-model.md))
-   **Response:** `JobSource` (see [Job Source Data Model](../data-models/job-source-model.md))

---

## Endpoints

### 1. Create a New Job Source

-   **Method:** `POST`
-   **Path:** `/`
-   **Description:** Creates a new job source record.
-   **Request Body:** `JobSourceCreate` schema.
-   **Response:** `201 Created` - Returns the created `JobSource` object.
-   **Example `curl`:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/job-srcs/" \
         -H "Content-Type: application/json" \
         -d '{
              "name": "LinkedIn Jobs",
              "type": "Job Board",
              "website": "https://linkedin.com/jobs"
            }'
    ```

### 2. Read All Job Sources

-   **Method:** `GET`
-   **Path:** `/`
-   **Description:** Retrieves a list of all job sources, with optional pagination.
-   **Query Parameters:**
    -   `skip` (int, optional, default: 0): Number of records to skip.
    -   `limit` (int, optional, default: 100): Maximum number of records to return.
-   **Response:** `200 OK` - Returns a list of `JobSource` objects.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/job-srcs/?skip=0&limit=10"
    ```

### 3. Read Job Source by ID

-   **Method:** `GET`
-   **Path:** `/{job_source_id}`
-   **Description:** Retrieves a single job source by its unique ID.
-   **Path Parameters:**
    -   `job_source_id` (int, required): The ID of the job source to retrieve.
-   **Response:**
    -   `200 OK` - Returns the `JobSource` object.
    -   `404 Not Found` - If the job source with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/job-srcs/1"
    ```

### 4. Update an Existing Job Source

-   **Method:** `PUT`
-   **Path:** `/{job_source_id}`
-   **Description:** Updates an existing job source.
-   **Path Parameters:**
    -   `job_source_id` (int, required): The ID of the job source to update.
-   **Request Body:** `JobSourceUpdate` schema. All fields are optional.
-   **Response:**
    -   `200 OK` - Returns the updated `JobSource` object.
    -   `404 Not Found` - If the job source does not exist.
    -   `400 Bad Request` - If there's a validation error (e.g., invalid type).
-   **Example `curl`:**
    ```bash
    curl -X PUT "http://localhost:8000/api/v1/job-srcs/1" \
         -H "Content-Type: application/json" \
         -d '{
              "name": "LinkedIn Job Postings",
              "notes": "Primary job board."
            }'
    ```

### 5. Delete a Job Source

-   **Method:** `DELETE`
-   **Path:** `/{job_source_id}`
-   **Description:** Deletes a job source by its ID.
-   **Path Parameters:**
    -   `job_source_id` (int, required): The ID of the job source to delete.
-   **Response:**
    -   `200 OK` - Returns the deleted `JobSource` object.
    -   `404 Not Found` - If the job source does not exist.
    -   `400 Bad Request` - If deletion is blocked due to existing relationships (e.g., job applications linked to this source).
-   **Example `curl`:**
    ```bash
    curl -X DELETE "http://localhost:8000/api/v1/job-srcs/1"
    ```

---

See also: [Job Source Data Model](../data-models/job-source-model.md) 