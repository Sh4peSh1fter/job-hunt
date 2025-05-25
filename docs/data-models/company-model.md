# Company Data Model

This document describes the structure and fields of the Company entity.

## Overview

Represents a company that has job openings or that the user is tracking.

## Backend Schema (`backend/app/schemas/company.py`)

-   **`CompanyBase`**
    -   `name` (str, required): The name of the company.
    -   `industry` (str, optional): The industry the company operates in.
    -   `website` (HttpUrl, optional): The company's official website URL.
    -   `linkedin_profile_url` (HttpUrl, optional): URL to the company's LinkedIn profile.
    -   `company_size` (str, optional): Approximate size of the company (e.g., "1-10 employees", "501-1000 employees").
    -   `founded_year` (int, optional): The year the company was founded.
    -   `headquarters_location` (str, optional): Location of the company's headquarters.
    -   `short_description` (str, optional): A brief description or tagline for the company.
    -   `notes` (str, optional): User's personal notes about the company.
    -   `culture_and_values` (str, optional): Notes on company culture and values.
    -   `benefits_overview` (str, optional): Overview of employee benefits.
    -   `hiring_process_insights` (str, optional): Insights into the company's hiring process.

-   **`CompanyCreate`** (inherits `CompanyBase`)
    -   All fields from `CompanyBase` are applicable for creation.

-   **`CompanyUpdate`** (all fields optional)
    -   `name` (str, optional)
    -   `industry` (str, optional)
    -   `website` (HttpUrl, optional)
    -   `linkedin_profile_url` (HttpUrl, optional)
    -   `company_size` (str, optional)
    -   `founded_year` (int, optional)
    -   `headquarters_location` (str, optional)
    -   `short_description` (str, optional)
    -   `notes` (str, optional)
    -   `culture_and_values` (str, optional)
    -   `benefits_overview` (str, optional)
    -   `hiring_process_insights` (str, optional)

-   **`Company`** (inherits `CompanyBase`)
    -   Includes all fields from `CompanyBase` plus:
    -   `id` (int, required): Auto-incrementing primary key.
    -   `created_at` (datetime, required): Timestamp of creation.
    -   `updated_at` (datetime, required): Timestamp of last update.

## Frontend Type (`frontend/src/lib/types.ts` - `CompanyDataItem`)

```typescript
export interface CompanyDataItem {
  id: number;
  name: string;
  industry?: string | null;
  website?: string | null;
  linkedin_profile_url?: string | null;
  company_size?: string | null;
  founded_year?: number | null;
  headquarters_location?: string | null;
  short_description?: string | null;
  notes?: string | null;
  culture_and_values?: string | null;
  benefits_overview?: string | null;
  hiring_process_insights?: string | null;
  created_at: string; // Represented as string after JSON serialization
  updated_at: string; // Represented as string after JSON serialization
}

// For Create/Update forms, often a Partial or specific type without id/timestamps
export type CompanyCreateData = Omit<CompanyDataItem, 'id' | 'created_at' | 'updated_at'>;
export type CompanyUpdateData = Partial<CompanyCreateData>;
```

## Database Table (Conceptual - managed by Alembic)

-   `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
-   `name` (VARCHAR, NOT NULL)
-   `industry` (VARCHAR)
-   `website` (VARCHAR)
-   `linkedin_profile_url` (VARCHAR)
-   `company_size` (VARCHAR)
-   `founded_year` (INTEGER)
-   `headquarters_location` (VARCHAR)
-   `short_description` (TEXT)
-   `notes` (TEXT)
-   `culture_and_values` (TEXT)
-   `benefits_overview` (TEXT)
-   `hiring_process_insights` (TEXT)
-   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
-   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

---

See also: [Companies API](../api/companies-api.md) 