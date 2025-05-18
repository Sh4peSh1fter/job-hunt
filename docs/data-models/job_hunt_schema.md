# Job Hunt Application - Data Schema

**Last Updated:** 18.5.2025

This document outlines the proposed database schema for the Job Hunt application. It defines the core entities, their attributes, and their relationships.  
To better understand what entities we should manage, lets try to see what scenarios are we taking part in while job hunting. The options that come to mind are:
1. There is a company which we are intrested in, and they have a job opening for what we are seeking.
2. There is a company which we are intrested in, but they don't have any relevant jobs for us.
3. There is a job source that we are following, and it has a job opening for us, and through it we learn about the company.
4. There is a job source that we are following, but it doesn't have any relevant jobs for us.

(job hunting options)[job-hunt-data-schema.png]

## Core Entities

The primary entities for managing the job search process are:

1.  **Company**: Information about companies.
2.  **JobApplication**: Tracking of applications made to job openings.
3.  **ApplicationEvent**: Timeline of events for each job application.
4.  **JobsSource**: List of job sources.

---

## Model Definitions

*(This section will be populated based on our discussion. For each model, we will define: Model Name, Description, Attributes/Fields, Relationships, and an optional Example.)*

### 1. Company

*   **Description:** Stores information about companies being tracked or applied to.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `name`: (String, required, unique)
    *   `foundation_date`: (DateTime, optional)
    *   `industry`: (String, optional)
    *   `size`: (String, optional, e.g., "1-50 employees", "50-200 employees")
    *   `phase`: (Enum: ["Pre-Seed", "Seed", "Early", "Growth", "Expansion", "Exit"], optional)
    *   `website`: (String, optional, URL validation)
    *   `linkedin`: (String, optional, URL validation) 
    *   `crunchbase`: (String, optional, URL validation) 
    *   `glassdoor`: (String, optional, URL validation)
    *   `short_description`: (String, optional)
    *   `notes`: (Text, optional) - General notes about the company.
    *   `related_articles`: (Text, optional) - List of URLs separated by commas.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   One-to-Many with `JobApplication` (A company can have multiple job applications).

### 2. JobApplication

*   **Description:** Stores details about a specific job role/position and tracks the user's application process.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `company_id`: (Foreign Key to `Company.id`, required)
    *   `title`: (String, required)
    *   `description_text`: (Text, optional) - The full job description.
    *   `job_url`: (String, required, URL validation)
    *   `location_city`: (String, optional)
    *   `location_country`: (String, optional)
    *   `is_remote`: (Boolean, default: `False`)
    *   `employment_type`: (Enum: ["Full-time", "Part-time", "Contract", "Internship", "Temporary", "Volunteer"], optional)
    *   `used_resume`: (String, optional) - Path to the resume version used.
    *   `cover_letter_file_path`: (String, optional) - Path to the cover letter version used.
    *   `requested_salary_min`: (Integer, optional)
    *   `requested_salary_max`: (Integer, optional)
    *   `salary_currency`: (String, optional, e.g., "USD", "ILS")
    *   `date_posted`: (Date, optional)
    *   `status`: (Enum: ["Considering", "Not Pursuing", "Applied", "In Progress", "Withdrawn", "Offered", "Rejected", "Expired"], default: "Considering") - User's private status for this opening.
    *   `discovered_through`: (Foreign Key to `JobSource.id`, required)
    *   `applied_through`: (String, optional) - e.g., "LinkedIn", "Company Website", "Referral", "Job Board".
    *   `referral`: (String, optional) - The name of the referral.
    *   `notes`: (Text, optional) - User's personal notes about this role.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `Company`.
    *   One-to-Many with `ApplicationEvent`.

### 3. ApplicationEvent

*   **Description:** Logs individual events or interactions related to a `JobApplication` timeline.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `job_application_id`: (Foreign Key to `JobApplication.id`, required)
    *   `event_type`: (Enum: ["Application Submitted", "Resume Viewed", "Screening Call Scheduled", "Screening Call Completed", "Technical Interview Scheduled", "Technical Interview Completed", "HR Interview Scheduled", "HR Interview Completed", "Take-home Assignment Sent", "Take-home Assignment Submitted", "Final Interview Scheduled", "Final Interview Completed", "Follow-up Sent", "Thank You Note Sent", "Offer Received", "Offer Terms Discussed", "Offer Accepted", "Offer Declined", "Application Withdrawn", "Rejection Received", "Feedback Requested", "Feedback Received", "Networking Call", "Informational Interview", "Note Added"], required)
    *   `event_date`: (DateTime, required, default: current timestamp)
    *   `participants`: (Text, required) - List of full names of the people who took part, separated by commas.
    *   `notes`: (Text, optional)
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `JobApplication`.

### 4. JobSource

*   **Description:** List of job sources.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `name`: (String, required, unique)
    *   `type`: (Enum: ["Job Board", "Recruiter", "Company Website", "Networking", "Referral Program", "Other"], optional)
    *   `website`: (String, optional, URL validation)
    *   `short_description`: (String, optional)
    *   `notes`: (Text, optional) - General notes about the company.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   One-to-Many with `JobApplication` (A job source can have multiple job applications).