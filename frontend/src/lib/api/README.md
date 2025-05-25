# Frontend API Utility Functions

This directory (`frontend/src/lib/api/`) contains TypeScript modules with functions dedicated to interacting with the backend API for specific data entities. These utilities encapsulate the `fetch` logic, request/response handling, and type definitions for API communication.

## Purpose

-   **Abstraction:** Provide a clean and abstracted interface for components to interact with backend services, without needing to know the specifics of `fetch` calls, headers, or URL construction.
-   **Type Safety:** Utilize TypeScript types (defined in `frontend/src/lib/types.ts` and specific to each API module) to ensure that data sent to and received from the API matches expected structures.
-   **Error Handling:** Implement basic error handling for API requests, typically by checking the HTTP response status and throwing an error if the request was not successful. This allows calling components to use `try...catch` blocks for managing API errors.
-   **Centralization:** Keep all API interaction logic for a given entity in one place, making it easier to manage and update if the backend API changes.

## Structure

Each file typically corresponds to a backend API resource (e.g., `company-api.ts` for company-related endpoints).

### Example: `company-api.ts`

-   **Base URL:** Defines the base path for the company API (e.g., `http://localhost:8000/api/v1/companies`).
-   **Functions:**
    -   `fetchCompanies()`: Fetches a list of all companies.
    -   `fetchCompanyById(id: number)`: Fetches a single company by its ID.
    -   `createCompany(companyData: CompanyCreateData)`: Creates a new company.
    -   `updateCompany(id: number, companyData: CompanyUpdateData)`: Updates an existing company.
    -   `deleteCompany(id: number)`: Deletes a company.
-   **Types:** May import or define specific request/response types if they are not already covered by the global types in `lib/types.ts`.

## General Usage

Page components (e.g., `frontend/src/app/(pages)/components/companies/page.tsx`) import and use these utility functions within their data fetching logic (e.g., in `useEffect` hooks) and event handlers (e.g., `handleAddCompany`, `handleUpdateCompany`).

```typescript
// Example usage in a component
import { fetchCompanies, createCompany } from '@/lib/api/company-api';
import { CompanyDataItem, CompanyCreateData } from '@/lib/types';

// ... inside a React component ...
useEffect(() => {
  const loadData = async () => {
    try {
      const companies = await fetchCompanies();
      setCompaniesData(companies);
    } catch (error) {
      console.error("Failed to fetch companies:", error);
      // Set error state
    }
  };
  loadData();
}, []);

const handleAddNewCompany = async (newCompanyData: CompanyCreateData) => {
  try {
    await createCompany(newCompanyData);
    // Refetch data or update local state
  } catch (error) {
    console.error("Failed to create company:", error);
    // Set error state for the form/dialog
  }
};
```

## Error Handling Convention

API utility functions generally check if `response.ok` is true. If not, they attempt to parse an error message from the response body (assuming a JSON response like `{ "detail": "Error message" }`) or use the response status text, and then throw an error. This allows the calling component to catch the error and display appropriate feedback to the user.

```typescript
// Simplified error handling example within an API util function
const response = await fetch(URL, { /* ...options... */ });
if (!response.ok) {
  let errorMessage = `HTTP error! status: ${response.status}`;
  try {
    const errorData = await response.json();
    errorMessage = errorData.detail || JSON.stringify(errorData);
  } catch (e) {
    // Could not parse JSON, use status text
    errorMessage = response.statusText;
  }
  throw new Error(errorMessage);
}
return response.json();
```

This centralized approach to API interaction helps maintain a clean and organized frontend codebase. 