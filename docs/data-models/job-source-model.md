# Job Source Data Model

This document describes the structure and fields of the Job Source entity.

## Overview

Represents the source through which a job opportunity was discovered (e.g., a specific job board, a recruiter, a company website).

## Backend Schema (`backend/app/schemas/job_source.py`)

-   **`JobSourceBase`**
    -   `name` (str, required): The name of the job source (e.g., "LinkedIn Jobs", "Indeed", "Tech Recruiter Inc.").
    -   `type` (JobSourceTypeEnum, optional): The type of job source (e.g., "Job Board", "Recruiter", "Company Website", "Networking", "Referral Program", "Other").
    -   `website` (HttpUrl, optional): URL for the job source, if applicable (e.g., the job board's website).
    -   `short_description` (str, optional): A brief description of the source.
    -   `notes` (str, optional): User's personal notes about this job source.

-   **`JobSourceCreate`** (inherits `JobSourceBase`)
    -   All fields from `JobSourceBase` are applicable for creation.

-   **`JobSourceUpdate`** (all fields optional)
    -   `name` (str, optional)
    -   `type` (JobSourceTypeEnum, optional)
    -   `website` (HttpUrl, optional)
    -   `short_description` (str, optional)
    -   `notes` (str, optional)

-   **`JobSource`** (inherits `JobSourceBase`)
    -   Includes all fields from `JobSourceBase` plus:
    -   `id` (int, required): Auto-incrementing primary key.
    -   `created_at` (datetime, required): Timestamp of creation.
    -   `updated_at` (datetime, required): Timestamp of last update.

## Frontend Type (`frontend/src/lib/types.ts` - `JobSource`)

```typescript
// Assuming JobSourceType is defined as a string literal union or enum

export interface JobSource {
  id: number;
  name: string;
  type?: JobSourceType | null; // e.g., "Job Board", "Recruiter"
  website?: string | null;
  short_description?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
}

export type JobSourceCreate = Omit<JobSource, 'id' | 'created_at' | 'updated_at'>;
export type JobSourceUpdate = Partial<JobSourceCreate>;
```

## Database Table (Conceptual)

-   `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
-   `name` (VARCHAR, NOT NULL)
-   `type` (VARCHAR) // Consider CHECK constraint for enum values
-   `website` (VARCHAR)
-   `short_description` (TEXT)
-   `notes` (TEXT)
-   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
-   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

---

See also: [Job Sources API](../api/job-sources-api.md) 