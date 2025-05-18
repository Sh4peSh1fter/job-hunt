# Companies API Endpoints

**Base Path:** `/api/v1/companies`

This document details the API endpoints available for managing company information.

---

## 1. Create a New Company

*   **Method & Path:** `POST /`
*   **Description:** Creates a new company record in the system.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `CompanyCreate` (see `backend/app/schemas/company.py`)
        ```json
        {
            "name": "Example Corp",
            "foundation_date": "2020-01-15T00:00:00",
            "industry": "Technology",
            "size": "50-200 employees",
            "phase": "Growth",
            "website": "https://examplecorp.com",
            "linkedin": "https://linkedin.com/company/examplecorp",
            "crunchbase": "https://crunchbase.com/organization/examplecorp",
            "glassdoor": "https://glassdoor.com/Overview/Working-at-Example-Corp-EI_IE12345.htm",
            "short_description": "A leading provider of innovative solutions.",
            "notes": "Met CEO at a conference.",
            "related_articles": "https://example.com/article1,https://example.com/article2"
        }
        ```
*   **Response:**
    *   **Success Code:** `201 Created`
    *   **Body Schema:** `Company` (see `backend/app/schemas/company.py`)
        ```json
        {
            "id": 1,
            "name": "Example Corp",
            "foundation_date": "2020-01-15T00:00:00",
            "industry": "Technology",
            // ... other fields ...
            "created_at": "2024-05-19T10:00:00Z",
            "updated_at": "2024-05-19T10:00:00Z"
        }
        ```
*   **Error Responses:**
    *   `422 Unprocessable Entity`: If request validation fails (e.g., missing required fields, invalid data types).

---

## 2. Read All Companies

*   **Method & Path:** `GET /`
*   **Description:** Retrieves a list of all companies, with optional pagination.
*   **Request Parameters (Query):**
    *   `skip` (integer, optional, default: 0): Number of records to skip for pagination.
    *   `limit` (integer, optional, default: 100): Maximum number of records to return.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `List[Company]` (a list of `Company` objects, see `backend/app/schemas/company.py`)
        ```json
        [
            {
                "id": 1,
                "name": "Example Corp",
                // ... other fields ...
            },
            {
                "id": 2,
                "name": "Another Ltd",
                // ... other fields ...
            }
        ]
        ```
*   **Error Responses:**
    *   `422 Unprocessable Entity`: If query parameters are invalid.

---

## 3. Read Company by ID

*   **Method & Path:** `GET /{company_id}`
*   **Description:** Retrieves a single company by its unique ID.
*   **Request Parameters (Path):**
    *   `company_id` (integer, required): The ID of the company to retrieve.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `Company` (see `backend/app/schemas/company.py`)
*   **Error Responses:**
    *   `404 Not Found`: If a company with the specified ID does not exist.
    *   `422 Unprocessable Entity`: If `company_id` is not a valid integer.

---

## 4. Update an Existing Company

*   **Method & Path:** `PUT /{company_id}`
*   **Description:** Updates an existing company's information. Only fields provided in the request body will be updated.
*   **Request Parameters (Path):**
    *   `company_id` (integer, required): The ID of the company to update.
*   **Request Body:**
    *   **Type:** `application/json`
    *   **Schema:** `CompanyUpdate` (see `backend/app/schemas/company.py`) - All fields are optional.
        ```json
        {
            "industry": "FinTech",
            "notes": "Updated notes: Pivoting to financial services."
        }
        ```
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `Company` (the updated company object)
*   **Error Responses:**
    *   `404 Not Found`: If a company with the specified ID does not exist.
    *   `422 Unprocessable Entity`: If `company_id` is invalid or request body validation fails.

---

## 5. Delete a Company

*   **Method & Path:** `DELETE /{company_id}`
*   **Description:** Deletes a company by its ID.
*   **Request Parameters (Path):**
    *   `company_id` (integer, required): The ID of the company to delete.
*   **Response:**
    *   **Success Code:** `200 OK`
    *   **Body Schema:** `Company` (the deleted company object)
    *   *Note: Could also be `204 No Content` with an empty body, but current implementation returns the deleted object.*
*   **Error Responses:**
    *   `404 Not Found`: If a company with the specified ID does not exist.
    *   `422 Unprocessable Entity`: If `company_id` is not a valid integer. 