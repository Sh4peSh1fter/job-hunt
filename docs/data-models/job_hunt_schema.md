# Job Hunt Application - Data Schema

**Last Updated:** October 26, 2023

This document outlines the proposed database schema for the Job Hunt application. It defines the core entities, their attributes, and their relationships.  
To better understand what entities we should manage, lets try to see what scenarios are we taking part in while job hunting. The options that come to mind are:
1. There is a company which we are intrested in, and they have a job opening for what we are seeking.
2. There is a company which we are intrested in, but they don't have any relevant jobs for us.
3. There is a jobs source that we are following, and it has a job opening for us, and through it we learn about the company.
4. There is a jobs source that we are following, but it doesn't have any relevant jobs for us.

(job hunting options)[job-hunt-data-schema.png]

## Core Entities

The primary entities for managing the job search process are:

1.  **Company**: Information about companies.
<!-- 2.  **JobOpening**: Details of specific job postings. -->
3.  **JobApplication**: Tracking of applications made to job openings.
<!-- 4.  **Contact**: Professional contacts. -->
5.  **ApplicationEvent**: Timeline of events for each job application.
<!-- 6.  **Skill** (Proposed): Skills relevant to job openings and possessed by the user.
7.  **Document** (Proposed): Storage or linkage to relevant documents like resumes and cover letters. -->

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
    <!-- *   `location_city`: (String, optional)
    *   `location_country`: (String, optional) -->
    *   `website`: (String, optional, URL validation)
    *   `linkedin`: (String, optional, URL validation) 
    *   `Crunchbase`: (String, optional, URL validation) 
    *   `glassdoor`: (String, optional, URL validation)
    *   `short_description`: (String, optional)
    *   `notes`: (Text, optional) - General notes about the company.
    *   `related_articles`: list of urls
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   One-to-Many with `JobOpening` (A company can have multiple job openings).
    <!-- *   One-to-Many with `Contact` (Multiple contacts can be associated with one company). -->

<!-- ### 2. JobOpening

*   **Description:** Stores details about a specific job role/position.
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
    *   `salary_min`: (Integer, optional)
    *   `salary_max`: (Integer, optional)
    *   `salary_currency`: (String, optional, e.g., "USD", "EUR")
    *   `date_posted`: (Date, optional)
    *   `date_closing`: (Date, optional)
    *   `internal_status`: (Enum: ["Tracking", "Considering", "Not Pursuing", "Expired"], default: "Tracking") - User's private status for this opening.
    *   `notes`: (Text, optional) - User's personal notes about this role.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `Company`.
    *   One-to-Many with `JobApplication` (One job opening can have one application from the user). -->

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
    *   `requested_salary`: (String, optional, e.g., "20,000 - 22,000")
    *   `salary_currency`: (String, optional, e.g., "USD", "ILS")
    *   `date_posted`: (Date, optional)
    *   `status`: (Enum: ["Considering", "Not Pursuing", "Applied", "In Progress", "Withdrawn", "Offered", "Rejected", "Expired"], default: "Considering") - User's private status for this opening.
    *   `applied_through`: (String, optional) - e.g., "LinkedIn", "Company Website", "Referral", "Job Board".
    *   `referral`: (String, optional) - The name of the referral.
    *   `notes`: (Text, optional) - User's personal notes about this role.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `Company`.
    *   One-to-Many with `ApplicationEvent`.

<!-- ### 4. Contact

*   **Description:** Manages professional contacts.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `first_name`: (String, required)
    *   `last_name`: (String, optional)
    *   `email`: (String, optional, unique if provided, email validation)
    *   `phone`: (String, optional)
    *   `linkedin_url`: (String, optional, URL validation)
    *   `current_company_id`: (Foreign Key to `Company.id`, optional)
    *   `current_role`: (String, optional)
    *   `notes`: (Text, optional) - How you met, conversation topics, etc.
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `Company` (for current employment).
    *   (Potentially) Many-to-Many with `JobApplication` (as a referral or interviewer). -->

### 3. ApplicationEvent

*   **Description:** Logs individual events or interactions related to a `JobApplication` timeline.
*   **Attributes/Fields:**
    *   `id`: (Primary Key, Integer, auto-incrementing)
    *   `job_application_id`: (Foreign Key to `JobApplication.id`, required)
    *   `event_type`: (Enum: ["Application Submitted", "Resume Viewed", "Screening Call Scheduled", "Screening Call Completed", "Technical Interview Scheduled", "Technical Interview Completed", "HR Interview Scheduled", "HR Interview Completed", "Take-home Assignment Sent", "Take-home Assignment Submitted", "Final Interview Scheduled", "Final Interview Completed", "Follow-up Sent", "Thank You Note Sent", "Offer Received", "Offer Terms Discussed", "Offer Accepted", "Offer Declined", "Application Withdrawn", "Rejection Received", "Feedback Requested", "Feedback Received", "Networking Call", "Informational Interview", "Note Added"], required)
    *   `event_date`: (DateTime, required, default: current timestamp)
    *   `participants`: (String, required) - Full names of the people who took part.
    *   `notes`: (Text, optional)
    <!-- *   `related_contact_id`: (Foreign Key to `Contact.id`, optional) - e.g., interviewer. -->
    *   `created_at`: (DateTime, auto-set on creation, not user-editable)
    *   `updated_at`: (DateTime, auto-set on update, not user-editable)
*   **Relationships:**
    *   Many-to-One with `JobApplication`.
    <!-- *   Many-to-One with `Contact` (optional). -->
