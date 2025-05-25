# Companies API

**Base Path:** `/api/v1/companies`

This API provides CRUD (Create, Read, Update, Delete) operations for company entities.

## Schemas

-   **Request (Create):** `CompanyCreate` (see [Company Data Model](../data-models/company-model.md))
-   **Request (Update):** `CompanyUpdate` (see [Company Data Model](../data-models/company-model.md))
-   **Response:** `Company` (see [Company Data Model](../data-models/company-model.md))

---

## Endpoints

### 1. Create a New Company

-   **Method:** `POST`
-   **Path:** `/`
-   **Description:** Creates a new company record.
-   **Request Body:** `CompanyCreate` schema.
-   **Response:** `201 Created` - Returns the created `Company` object.
-   **Example `curl`:**
    ```bash
    curl -X POST "http://localhost:8000/api/v1/companies/" \
         -H "Content-Type: application/json" \
         -d '{
              "name": "Innovate Solutions Inc.",
              "industry": "Technology",
              "website": "https://innovatesolutions.example.com"
            }'
    ```

### 2. Read All Companies

-   **Method:** `GET`
-   **Path:** `/`
-   **Description:** Retrieves a list of all companies, with optional pagination.
-   **Query Parameters:**
    -   `skip` (int, optional, default: 0): Number of records to skip.
    -   `limit` (int, optional, default: 100): Maximum number of records to return.
-   **Response:** `200 OK` - Returns a list of `Company` objects.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/companies/?skip=0&limit=10"
    ```

### 3. Read Company by ID

-   **Method:** `GET`
-   **Path:** `/{company_id}`
-   **Description:** Retrieves a single company by its unique ID.
-   **Path Parameters:**
    -   `company_id` (int, required): The ID of the company to retrieve.
-   **Response:**
    -   `200 OK` - Returns the `Company` object.
    -   `404 Not Found` - If the company with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X GET "http://localhost:8000/api/v1/companies/1"
    ```

### 4. Update an Existing Company

-   **Method:** `PUT`
-   **Path:** `/{company_id}`
-   **Description:** Updates an existing company's information.
-   **Path Parameters:**
    -   `company_id` (int, required): The ID of the company to update.
-   **Request Body:** `CompanyUpdate` schema. All fields are optional; only provided fields will be updated.
-   **Response:**
    -   `200 OK` - Returns the updated `Company` object.
    -   `404 Not Found` - If the company with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X PUT "http://localhost:8000/api/v1/companies/1" \
         -H "Content-Type: application/json" \
         -d '{
              "industry": "Advanced Technology",
              "notes": "Updated notes for Innovate Solutions."
            }'
    ```

### 5. Delete a Company

-   **Method:** `DELETE`
-   **Path:** `/{company_id}`
-   **Description:** Deletes a company by its ID.
-   **Path Parameters:**
    -   `company_id` (int, required): The ID of the company to delete.
-   **Response:**
    -   `200 OK` - Returns the deleted `Company` object.
    -   `404 Not Found` - If the company with the specified ID does not exist.
-   **Example `curl`:**
    ```bash
    curl -X DELETE "http://localhost:8000/api/v1/companies/1"
    ```

---

See also: [Company Data Model](../data-models/company-model.md) 