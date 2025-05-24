# Frontend: Data Component Pages

**Last Updated:** May 21, 2024

This document details the structure and functionality of the "Components" section of the frontend application, specifically focusing on how data entities are displayed and managed. The `CompaniesTable` and its associated features serve as the primary example and pattern for other data entity tables (Job Applications, Application Events, Job Sources).

## 1. Overview

The `/components` route in the application serves as a hub page. It displays cards or links for each core data entity defined in the backend (e.g., Companies, Job Applications). Clicking on one of these links navigates the user to a dedicated page for that entity, where they can view, manage, and interact with the data.

Each individual data entity page (e.g., `/components/companies`) primarily features a table that lists all records for that entity and provides CRUD (Create, Read, Update, Delete) functionalities.

## 2. Core Data Table Component: `CompaniesTable.tsx` Example

The `frontend/src/components/specific/companies-table.tsx` component is responsible for fetching, displaying, and managing company data.

### 2.1. Purpose

-   Display a paginated/scrollable list of all company records.
-   Allow users to view detailed information for a single company.
-   Enable inline editing of company records.
-   Provide a mechanism to delete company records with confirmation.

### 2.2. Key Features Implemented

-   **Data Fetching:** Asynchronously fetches company data from the backend API (`/api/v1/companies/`) on component mount.
-   **Tabular Display:** Uses Shadcn/UI `Table` component to render data.
-   **View Details:** A "View" button for each row opens a `CompanyViewDialog` modal displaying all fields of the selected company (excluding ID).
-   **Inline Editing:**
    -   An "Edit" button toggles the row into an editable state.
    -   Input fields (`<Input type="text">`, `<Input type="date">`) appear for editable columns.
    -   "Save" and "Cancel" buttons manage the editing process.
    -   Changes are sent to the backend via a `PUT` request.
-   **Deletion:**
    -   A "Delete" button opens a `CompanyDeleteDialog` for confirmation.
    -   Confirmed deletions trigger a `DELETE` request to the backend.

### 2.3. State Management (Key Variables)

-   `companies: Company[]`: Stores the array of company objects fetched from the backend.
-   `loading: boolean`: Tracks the loading state for data fetching.
-   `error: string | null`: Stores error messages related to data fetching or updates.
-   `selectedCompanyForView: Company | null`: Holds the company object currently being viewed in the dialog.
-   `isViewDialogOpen: boolean`: Controls the visibility of the `CompanyViewDialog`.
-   `editingCompanyId: number | null`: Stores the ID of the company currently being edited inline. If `null`, no company is in edit mode.
-   `editedCompanyData: Partial<Company> | null`: Holds the modified data for the company being edited before saving.
-   `companyToDelete: Company | null`: Holds the company object selected for deletion.
-   `isDeleteDialogOpen: boolean`: Controls the visibility of the `CompanyDeleteDialog`.

### 2.4. Helper Functions & Event Handlers

-   `fetchCompanies(): Promise<Company[]>`: Fetches all companies from the backend.
-   `updateCompanyOnBackend(id: number, data: Partial<Company>): Promise<Company | null>`: Sends a `PUT` request to update a company.
-   `deleteCompanyOnBackend(id: number): Promise<boolean>`: Sends a `DELETE` request to remove a company.
-   `handleViewCompany(company: Company)`: Sets state to open the view dialog for the selected company.
-   `handleEditCompany(company: Company)`: Sets state to activate inline editing for the selected company.
-   `handleCancelEdit()`: Resets editing state, discarding changes.
-   `handleSaveEdit()`: Calls `updateCompanyOnBackend` and updates local state upon success.
-   `handleInputChange(event)`: Updates `editedCompanyData` as the user types in inline input fields.
-   `handleOpenDeleteDialog(company: Company)`: Sets state to open the delete confirmation dialog.
-   `handleConfirmDelete(companyId: number)`: Calls `deleteCompanyOnBackend` and updates local state upon success.

### 2.5. Rendering Logic

-   `renderCellContent(content, fieldName, companyId)`: This crucial function determines how each cell's content is rendered.
    -   If `editingCompanyId` matches the `companyId` for the current row, and the `fieldName` is editable, it renders an `<Input>` component.
    -   Otherwise, it displays the data. It includes logic to render website/LinkedIn links as clickable `<a>` tags and formats date/datetime strings.

## 3. Dialog Components

Reusable dialogs are used for viewing and confirming deletions.

### 3.1. `CompanyViewDialog.tsx`

-   **Path:** `frontend/src/components/specific/company-view-dialog.tsx`
-   **Purpose:** Displays all details of a selected company in a modal dialog.
-   **Props:**
    -   `company: Company | null`: The company object to display.
    -   `isOpen: boolean`: Controls dialog visibility.
    -   `onOpenChange: (isOpen: boolean) => void`: Callback to handle dialog open/close state changes.
-   **Functionality:** Renders company fields with labels. Formats dates and clickable links appropriately. Excludes the `ID` field.

### 3.2. `CompanyDeleteDialog.tsx`

-   **Path:** `frontend/src/components/specific/company-delete-dialog.tsx`
-   **Purpose:** Provides a confirmation step before deleting a company.
-   **Props:**
    -   `company: Company | null`: The company object targeted for deletion (used to display name/ID in confirmation).
    -   `isOpen: boolean`: Controls dialog visibility.
    -   `onOpenChange: (isOpen: boolean) => void`: Callback for dialog state.
    -   `onConfirmDelete: (companyId: number) => void`: Callback executed when the user confirms deletion.
-   **Functionality:** Shows a warning message and requires explicit confirmation. The "Delete" action button has a destructive visual style.

## 4. Styling

-   Primarily uses **Shadcn/UI** components (`Table`, `Button`, `Input`, `Dialog`, `AlertDialog`). These components are built with **Tailwind CSS**.
-   Custom styling is minimal and achieved through Tailwind utility classes directly in the JSX or within Shadcn/UI component modifications if necessary.
-   `overflow-x-auto` is used on the table container to handle wide tables with many columns.

## 5. API Interaction

-   **GET `/api/v1/companies/`**: Fetches all companies.
-   **PUT `/api/v1/companies/{id}`**: Updates a specific company. Expects a JSON body with fields to be updated.
-   **DELETE `/api/v1/companies/{id}`**: Deletes a specific company.

Error handling for API requests is currently basic (console logs). For production, this should be enhanced with user-facing notifications (e.g., toasts).

## 6. Future Enhancements & Considerations for Other Data Tables

When implementing tables for other data entities (Job Applications, Application Events, Job Sources), the `CompaniesTable` structure can serve as a template. However, consider the following:

-   **Textarea for Longer Inputs:** For fields like "Notes" or detailed descriptions, using `<Textarea />` (from Shadcn/UI, if not already added) instead of `<Input />` during inline editing would be more appropriate.
-   **Select for Enum/Constrained Fields:** For fields with predefined choices (e.g., "Phase", "Size", or status fields in other entities), using a `<Select />` component (from Shadcn/UI) populated with these choices would improve the editing experience and data integrity.
-   **Date/Time Pickers:** For more complex date/time inputs, dedicated picker components could be integrated.
-   **Client-Side Validation:** While backend validation is key, adding client-side validation (e.g., with `zod` and `react-hook-form`, though `react-hook-form` might be overkill for simple inline editing) can improve UX.
-   **User Feedback:** Implement toast notifications or other clear visual feedback for successful operations (save, delete) and for errors.
-   **Generic Table Component:** If many data tables share almost identical CRUD logic, consider abstracting parts into a more generic, reusable table component or set of hooks to reduce code duplication. This would involve passing configurations for columns, API endpoints, and data types.
-   **Pagination/Virtualization:** For very large datasets, implement server-side pagination or frontend virtualization techniques to maintain performance. The current implementation loads all data at once.
-   **Sorting and Filtering:** Add client-side or server-side sorting and filtering capabilities to the tables.

This documentation should provide a good starting point for developers to understand and extend the data management features of the frontend. 