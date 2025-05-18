# Job Sources API Endpoints

**Base Path:** `/api/v1/job_sources`

This document details the API endpoints for managing job sources (e.g., job boards, recruiters).

---

## 1. Create a New Job Source

*   **Method & Path:** `POST /`
*   **Description:** Creates a new job source.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `JobSourceCreate` (see `backend/app/schemas/job_source.py`)
        ```json
        {
            "name": "LinkedIn Jobs",
            "type": "Job Board",
            "website": "https://www.linkedin.com/jobs/",
            "short_description": "Professional networking and job searching platform."
        }
        ```
*   **Response:**
    *   **Success Code:** `201 Created`
    *   **Body Schema:** `JobSource` (see `backend/app/schemas/job_source.py`)
*   **Error Responses:**
    *   `400 Bad Request`: If a job source with the same name already exists (due to `ValueError` from service).
    *   `422 Unprocessable Entity`: If request validation fails.

---

## 2. Read All Job Sources

*   **Method & Path:** `GET /`
*   **Description:** Retrieves a list of all job sources, with optional pagination.
*   **Request Parameters (Query):**
    *   `skip` (integer, optional, default: 0): Number of records to skip.
    *   `limit` (integer, optional, default: 100): Maximum number of records to return.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `List[JobSource]`
*   **Error Responses:**
    *   `422 Unprocessable Entity`: If query parameters are invalid.

---

## 3. Read Job Source by ID

*   **Method & Path:** `GET /{job_source_id}`
*   **Description:** Retrieves a single job source by its ID.
*   **Request Parameters (Path):**
    *   `job_source_id` (integer, required): The ID of the job source.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobSource`
*   **Error Responses:**
    *   `404 Not Found`: If the job source does not exist.
    *   `422 Unprocessable Entity`: If `job_source_id` is invalid.

---

## 4. Update an Existing Job Source

*   **Method & Path:** `PUT /{job_source_id}`
*   **Description:** Updates an existing job source. Only provided fields are updated.
*   **Request Parameters (Path):**
    *   `job_source_id` (integer, required): The ID of the job source to update.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `JobSourceUpdate` (see `backend/app/schemas/job_source.py`) - All fields optional.
        ```json
        {
            "name": "LinkedIn Super Jobs",
            "notes": "Updated branding."
        }
        ```
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobSource` (the updated job source object)
*   **Error Responses:**
    *   `400 Bad Request`: If updating the name conflicts with another existing job source name.
    *   `404 Not Found`: If the job source with the specified ID does not exist.
    *   `422 Unprocessable Entity`: If `job_source_id` is invalid or request body validation fails.

---

## 5. Delete a Job Source

*   **Method & Path:** `DELETE /{job_source_id}`
*   **Description:** Deletes a job source by its ID.
*   **Request Parameters (Path):**
    *   `job_source_id` (integer, required): The ID of the job source to delete.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobSource` (the deleted job source object)
*   **Error Responses:**
    *   `400 Bad Request`: If the job source is referenced by job applications and cannot be deleted (if service layer enforces this).
    *   `404 Not Found`: If the job source does not exist.
    *   `422 Unprocessable Entity`: If `job_source_id` is invalid. 