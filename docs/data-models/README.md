# Data Models

This section describes the core data entities used within the Job Hunt application. These models are represented as Pydantic schemas in the backend (`backend/app/schemas/`) and are used for API request/response validation and data structuring. Corresponding TypeScript types are defined in the frontend (`frontend/src/lib/types.ts`).

## Core Entities

-   [Company Model](./company-model.md)
-   [Job Application Model](./job-application-model.md)
-   [Job Source Model](./job-source-model.md)
-   [Application Event Model](./application-event-model.md) (Placeholder, not yet fully implemented or exposed via API)

## Relationships

-   A **Job Application** belongs to one **Company** (`company_id`).
-   A **Job Application** is discovered through one **Job Source** (`discovered_through_id`).
-   (Future) An **Application Event** will belong to one **Job Application**.

## Backend Schemas (`backend/app/schemas/`)

For each entity, there are typically three types of Pydantic schemas:

1.  **`EntityBase`**: Contains common fields shared by create and read schemas.
2.  **`EntityCreate`**: Inherits from `EntityBase` and includes fields required for creating a new entity. Excludes fields like `id`, `created_at`, `updated_at` that are auto-generated.
3.  **`EntityUpdate`**: Contains all fields from `EntityBase` but makes them optional, allowing partial updates.
4.  **`Entity`** (or `EntityRead`): Inherits from `EntityBase` and includes fields like `id`, `created_at`, `updated_at`. This is typically the schema used for API responses.

## Frontend Types (`frontend/src/lib/types.ts`)

TypeScript interfaces and types are defined to mirror the backend schemas, ensuring type safety when interacting with the API and managing data in the frontend components. 