# Website Navigation and Pages Plan

**Last Updated:** May 20, 2024

This document outlines the proposed navigation structure and page layout for the Job Hunt application. It aims to provide a clear and intuitive way for users to access all features and manage their job search data effectively.

## 1. Core Principles

-   **Data-Centric Navigation:** Key data entities defined in `docs/data-models/job_hunt_schema.md` should be easily accessible.
-   **Task-Oriented Tools:** The "Tools" section should remain a distinct area for specialized functionalities.
-   **Clear Guidance:** The "Guide" should be readily available for users seeking help or best practices.
-   **Scalability:** The navigation should be able to accommodate future features and data types.

## 2. Proposed Top-Level Navigation

Based on current features and the data model, the main navigation tabs could be:

1.  **Dashboard/Overview:** (Potentially the current "Job Applications" page, or a new higher-level dashboard)
    -   Summary of ongoing applications, upcoming events, key stats.
2.  **Job Applications:** (Already created as ` /applications`)
    -   Detailed list/table of all job applications.
    -   Ability to view, add, edit, and manage individual applications and their events.
3.  **Companies:**
    -   List/table of all tracked companies.
    -   Ability to view, add, edit company details and see related applications.
4.  **Job Sources:**
    -   List/table of all job sources.
    -   Ability to view, add, edit job source details and see related applications.
5.  **Tools:** (Existing `/tools` page)
    -   Access to Keyword Frequency Analyzer, Company Research Assistant (planned), etc.
6.  **Guide:** (Existing `/` or `/guide` page)
    -   Static content providing job search advice and application usage tips.

*Open Question: Should "Application Events" be a top-level item, or primarily accessed via a specific Job Application? Given the schema, accessing via Job Application seems more logical.* 

## 3. Page Breakdown by Data Entity

This section will detail the specific views and functionalities for each data model.

### 3.1. Companies

-   **List View (`/companies`):**
    -   Table/Card display of all companies (Name, Industry, Size, # of Applications).
    -   Search and filtering capabilities.
    -   Link to add a new company.
-   **Detail View (`/companies/{id}`):
    -   Full company details (all fields from schema).
    -   List of job applications associated with this company.
    -   Ability to edit company details.
    -   Ability to add a new job application pre-filled with this company.
-   **Add/Edit Form (`/companies/new`, `/companies/{id}/edit`):
    -   Form to input/modify all company fields.

### 3.2. Job Applications

-   **List View (`/applications` - current dashboard):
    -   Table/Card display of all job applications (Title, Company, Status, Date Applied).
    -   Advanced search and filtering (by status, company, date range, etc.).
    -   Link to add a new job application.
-   **Detail View (`/applications/{id}`):
    -   Full job application details.
    -   Timeline of `ApplicationEvents` associated with this application.
    -   Ability to add new `ApplicationEvent`.
    -   Ability to edit job application details.
-   **Add/Edit Form (`/applications/new`, `/applications/{id}/edit`):
    -   Form to input/modify all job application fields.

### 3.3. Application Events

-   **Primarily accessed via Job Application Detail View.**
-   **Add/Edit Form (Modal or separate page `/applications/{app_id}/events/new`, `/applications/{app_id}/events/{event_id}/edit`):
    -   Form to input/modify event details (type, date, notes).

### 3.4. Job Sources

-   **List View (`/jobsources`):
    -   Table/Card display of all job sources (Name, Type, Website).
    -   Search and filtering.
    -   Link to add a new job source.
-   **Detail View (`/jobsources/{id}`):
    -   Full job source details.
    -   List of job applications discovered through this source.
    -   Ability to edit job source details.
-   **Add/Edit Form (`/jobsources/new`, `/jobsources/{id}/edit`):
    -   Form to input/modify all job source fields.

## 4. Navbar Structure Considerations

-   **Current Frontend (`frontend/src/app/layout.tsx`):** Uses a simple header with direct links.
    ```tsx
    <nav className="ml-auto flex gap-4 sm:gap-6">
      <Link href="/">Guide</Link>
      <Link href="/tools">Tools</Link>
      <Link href="/applications">Job Applications</Link>
      {/* Future links for Companies, Job Sources would go here */}
    </nav>
    ```
-   **Backend Structure (`backend/`):** Provides API endpoints for CRUD operations on these data models. The frontend will interact with these APIs.
-   **Proposed Navbar Items:**
    -   Dashboard (or Applications)
    -   Companies
    -   Job Sources
    -   Tools
    -   Guide

## 5. Discussion Points & Open Questions

-   What should be the primary landing page after login (if auth is implemented)? For now, the "Guide" or "Applications Dashboard" are candidates.
-   How do we handle the display of many `ApplicationEvents`? Pagination or infinite scroll on the Job Application detail page?
-   Should there be a global search functionality?
-   Confirm naming for URLs (e.g., `/jobsources` vs `/sources`).

This document will be updated as the discussion progresses and decisions are made.

## 6. Alternative Navigation Proposal (Option 2 - User Suggested)

This alternative proposal offers a different grouping for accessing data entities.

### 6.1. Top-Level Navigation (Option 2)

1.  **Dashboard (`/dashboard`):**
    -   Serves as the main overview page. Could include summaries, key statistics, upcoming `ApplicationEvents`, and quick links.
2.  **Components (`/components`):
    -   A central page that acts as a directory to all core data entities.
    -   Displays sections/cards for: Companies, Job Applications, Application Events, Job Sources.
    -   Layout could be similar to the current `/tools` page, where each card links to a dedicated page for that data entity.
3.  **Tools (`/tools`):**
    -   Existing tools section, providing access to specialized functionalities like Keyword Analyzer, etc.
4.  **Guide (`/` or `/guide`):
    -   Existing guide section for help and best practices.

### 6.2. Page Breakdown (Option 2)

#### `/components` Page:

-   Links to the following individual component pages.

#### Individual Component Pages (Data Entity Views):

-   **General Structure:** Each page (e.g., `/components/companies`, `/components/job-applications`) would feature:
    -   A main title (e.g., "Companies Data", "Job Applications Log").
    -   A button to "Add New [Entity]".
    -   A comprehensive table displaying all records for that entity. The columns should directly mirror the fields in the `docs/data-models/job_hunt_schema.md` for that entity.
    -   Each row in the table should have actions (e.g., View Details, Edit, Delete).
    -   Search and filtering capabilities for the table.

-   **Specific Component Pages:**
    -   **`/components/companies`**: Table of all `Company` records.
        -   Detail View: `/components/companies/{id}`
        -   Add Form: `/components/companies/new`
        -   Edit Form: `/components/companies/{id}/edit`
    -   **`/components/job-applications`**: Table of all `JobApplication` records.
        -   Detail View: `/components/job-applications/{id}` (this view would also show related `ApplicationEvents`)
        -   Add Form: `/components/job-applications/new`
        -   Edit Form: `/components/job-applications/{id}/edit`
    -   **`/components/application-events`**: Table of all `ApplicationEvent` records.
        -   Detail View: `/components/application-events/{id}` (potentially less critical if events are mainly viewed via Job Application)
        -   Add Form: `/components/application-events/new` (likely accessed via a specific Job Application)
        -   Edit Form: `/components/application-events/{id}/edit`
    -   **`/components/job-sources`**: Table of all `JobSource` records.
        -   Detail View: `/components/job-sources/{id}`
        -   Add Form: `/components/job-sources/new`
        -   Edit Form: `/components/job-sources/{id}/edit`

### 6.3. Navbar Structure (Option 2)

```tsx
<nav className="ml-auto flex gap-4 sm:gap-6">
  <Link href="/dashboard">Dashboard</Link>
  <Link href="/components">Components</Link>
  <Link href="/tools">Tools</Link>
  <Link href="/">Guide</Link> // Or /guide
</nav>
```

### 6.4. Considerations for Option 2

-   **Pros:**
    -   Keeps top-level navigation very concise.
    -   Scales well if more data entities or tools are added; they can be listed on the `/components` or `/tools` pages respectively without cluttering the main navbar.
    -   Provides a clear separation between high-level dashboard, data management, functional tools, and guidance.
-   **Cons:**
    -   Adds an extra click to reach specific data tables (e.g., Dashboard -> Components -> Companies vs. Dashboard -> Companies).
    -   The `/components/application-events` page might become very long and less useful if not heavily filtered or contextualized, reinforcing the idea that events are best viewed within their parent `JobApplication`. 