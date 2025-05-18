# Job Applications API Endpoints

**Base Path:** `/api/v1/job_applications`

This document details the API endpoints for managing job applications.

---

## 1. Create a New Job Application

*   **Method & Path:** `POST /`
*   **Description:** Creates a new job application linked to an existing company and job source.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `JobApplicationCreate` (see `backend/app/schemas/job_application.py`)
        ```json
        {
            "company_id": 1,
            "title": "Software Engineer",
            "description_text": "Looking for a skilled software engineer...",
            "job_url": "https://example.com/job/swe123",
            "location_city": "San Francisco",
            "location_country": "USA",
            "is_remote": false,
            "employment_type": "Full-time",
            "status": "Applied",
            "discovered_through_id": 1
        }
        ```
*   **Response:**
    *   **Success Code:** `201 Created`
    *   **Body Schema:** `JobApplication` (see `backend/app/schemas/job_application.py`)
*   **Error Responses:**
    *   `404 Not Found`: If the specified `company_id` or `discovered_through_id` does not exist.
    *   `422 Unprocessable Entity`: If request validation fails.

---

## 2. Read All Job Applications

*   **Method & Path:** `GET /`
*   **Description:** Retrieves a list of all job applications, with optional pagination.
*   **Request Parameters (Query):**
    *   `skip` (integer, optional, default: 0): Number of records to skip.
    *   `limit` (integer, optional, default: 100): Maximum number of records to return.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `List[JobApplication]`
*   **Error Responses:**
    *   `422 Unprocessable Entity`: If query parameters are invalid.

---

## 3. Read Job Application by ID

*   **Method & Path:** `GET /{job_application_id}`
*   **Description:** Retrieves a single job application by its ID.
*   **Request Parameters (Path):**
    *   `job_application_id` (integer, required): The ID of the job application.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobApplication`
*   **Error Responses:**
    *   `404 Not Found`: If the job application does not exist.
    *   `422 Unprocessable Entity`: If `job_application_id` is invalid.

---

## 4. Update an Existing Job Application

*   **Method & Path:** `PUT /{job_application_id}`
*   **Description:** Updates an existing job application. Only provided fields are updated.
*   **Request Parameters (Path):**
    *   `job_application_id` (integer, required): The ID of the job application to update.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `JobApplicationUpdate` (see `backend/app/schemas/job_application.py`) - All fields optional.
        ```json
        {
            "title": "Senior Software Engineer",
            "status": "In Progress",
            "notes": "Followed up with hiring manager."
        }
        ```
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobApplication` (the updated job application object)
*   **Error Responses:**
    *   `404 Not Found`: If the job application, or a referenced `company_id` or `discovered_through_id` (if being updated) does not exist.
    *   `422 Unprocessable Entity`: If `job_application_id` is invalid or request body validation fails.

---

## 5. Delete a Job Application

*   **Method & Path:** `DELETE /{job_application_id}`
*   **Description:** Deletes a job application by its ID.
*   **Request Parameters (Path):**
    *   `job_application_id` (integer, required): The ID of the job application to delete.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `JobApplication` (the deleted job application object)
*   **Error Responses:**
    *   `404 Not Found`: If the job application does not exist.
    *   `422 Unprocessable Entity`: If `job_application_id` is invalid. 