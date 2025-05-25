# Job Application Data Model

This document describes the structure and fields of the Job Application entity.

## Overview

Represents a specific job application submitted by the user to a company for a particular role.

## Backend Schema (`backend/app/schemas/job_application.py`)

-   **`JobApplicationBase`**
    -   `company_id` (int, required): Foreign key referencing the `Company` this application is for.
    -   `title` (str, required): The job title applied for.
    -   `job_url` (HttpUrl, optional): Direct URL to the job posting.
    -   `status` (JobApplicationStatusEnum, required): Current status of the application (e.g., "Draft", "Applied", "Interviewing", "Offer", "Rejected", "Withdrawn").
    -   `date_posted` (date, optional): The date the job was posted.
    -   `date_applied` (date, optional): The date the user applied.
    -   `date_last_status_change` (date, optional): Date of the most recent status update.
    -   `salary_expectation_low` (int, optional): Lower bound of salary expectation.
    -   `salary_expectation_high` (int, optional): Upper bound of salary expectation.
    -   `salary_currency` (str, optional): Currency for salary expectations (e.g., "USD").
    -   `location` (str, optional): Job location (e.g., "Remote", "City, State").
    -   `employment_type` (EmploymentTypeEnum, optional): Type of employment (e.g., "Full-time", "Contract").
    -   `discovered_through_id` (int, optional): Foreign key referencing the `JobSource` where this job was found.
    -   `cover_letter_text` (str, optional): Text of the cover letter submitted.
    -   `resume_version` (str, optional): Identifier for the resume version used.
    -   `notes` (str, optional): User's general notes about this application.

-   **`JobApplicationCreate`** (inherits `JobApplicationBase`)
    -   All fields from `JobApplicationBase` are applicable.

-   **`JobApplicationUpdate`** (all fields optional)
    -   `company_id` (int, optional)
    -   `title` (str, optional)
    -   `job_url` (HttpUrl, optional)
    -   `status` (JobApplicationStatusEnum, optional)
    -   `date_posted` (date, optional)
    -   `date_applied` (date, optional)
    -   `date_last_status_change` (date, optional)
    -   `salary_expectation_low` (int, optional)
    -   `salary_expectation_high` (int, optional)
    -   `salary_currency` (str, optional)
    -   `location` (str, optional)
    -   `employment_type` (EmploymentTypeEnum, optional)
    -   `discovered_through_id` (int, optional)
    -   `cover_letter_text` (str, optional)
    -   `resume_version` (str, optional)
    -   `notes` (str, optional)

-   **`JobApplication`** (inherits `JobApplicationBase`)
    -   Includes all fields from `JobApplicationBase` plus:
    -   `id` (int, required): Auto-incrementing primary key.
    -   `created_at` (datetime, required): Timestamp of creation.
    -   `updated_at` (datetime, required): Timestamp of last update.
    -   `company` (Company, optional): Nested `Company` object (if loaded with relationship).
    -   `discovered_through` (JobSource, optional): Nested `JobSource` object (if loaded with relationship).
    -   `events` (List[ApplicationEvent], optional): List of related `ApplicationEvent` objects (if loaded).

## Frontend Type (`frontend/src/lib/types.ts` - `JobApplication`)

```typescript
// Assuming JobApplicationStatus and EmploymentType are defined string literal unions or enums

export interface JobApplication {
  id: number;
  company_id: number;
  title: string;
  job_url?: string | null;
  status: JobApplicationStatus; // e.g., "Applied", "Interviewing"
  date_posted?: string | null; // ISO date string
  date_applied?: string | null; // ISO date string
  date_last_status_change?: string | null; // ISO date string
  salary_expectation_low?: number | null;
  salary_expectation_high?: number | null;
  salary_currency?: string | null;
  location?: string | null;
  employment_type?: EmploymentType | null; // e.g., "Full-time", "Contract"
  discovered_through_id?: number | null;
  cover_letter_text?: string | null;
  resume_version?: string | null;
  notes?: string | null;
  created_at: string;
  updated_at: string;
  // Optional nested objects if fetched with joins:
  company?: CompanyDataItem | null; 
  discovered_through?: JobSource | null;
}

export type JobApplicationCreateData = Omit<JobApplication, 'id' | 'created_at' | 'updated_at' | 'company' | 'discovered_through'>;
export type JobApplicationUpdateData = Partial<JobApplicationCreateData>;
```

## Database Table (Conceptual)

-   `id` (INTEGER, PRIMARY KEY, AUTOINCREMENT)
-   `company_id` (INTEGER, FOREIGN KEY -> companies.id)
-   `title` (VARCHAR, NOT NULL)
-   `job_url` (VARCHAR)
-   `status` (VARCHAR, NOT NULL)  // Consider CHECK constraint for enum values
-   `date_posted` (DATE)
-   `date_applied` (DATE)
-   `date_last_status_change` (DATE)
-   `salary_expectation_low` (INTEGER)
-   `salary_expectation_high` (INTEGER)
-   `salary_currency` (VARCHAR)
-   `location` (VARCHAR)
-   `employment_type` (VARCHAR) // Consider CHECK constraint for enum values
-   `discovered_through_id` (INTEGER, FOREIGN KEY -> job_sources.id)
-   `cover_letter_text` (TEXT)
-   `resume_version` (VARCHAR)
-   `notes` (TEXT)
-   `created_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
-   `updated_at` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

---

See also: [Job Applications API](../api/job-applications-api.md) 