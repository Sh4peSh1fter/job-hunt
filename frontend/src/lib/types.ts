// Global type definitions for the Job Hunt project

// -------------- ENUM TYPES (mirroring backend enums) --------------
// These can be expanded or directly used as string literal unions in interfaces.
// For now, we'll use string literal unions where appropriate.

export type CompanyPhase = "Pre-Seed" | "Seed" | "Early" | "Growth" | "Expansion" | "Exit";
export type EmploymentType = "Full-time" | "Part-time" | "Contract" | "Internship" | "Temporary" | "Volunteer";
export type ApplicationStatus = "Considering" | "Not Pursuing" | "Applied" | "In Progress" | "Withdrawn" | "Offered" | "Rejected" | "Expired";
export type JobSourceType = "Job Board" | "Recruiter" | "Company Website" | "Networking" | "Referral Program" | "Other";
export type ApplicationEventType = 
  | "Application Submitted" | "Resume Viewed" | "Screening Call Scheduled" | "Screening Call Completed" 
  | "Technical Interview Scheduled" | "Technical Interview Completed" | "HR Interview Scheduled" 
  | "HR Interview Completed" | "Take-home Assignment Sent" | "Take-home Assignment Submitted" 
  | "Final Interview Scheduled" | "Final Interview Completed" | "Follow-up Sent" | "Thank You Note Sent" 
  | "Offer Received" | "Offer Terms Discussed" | "Offer Accepted" | "Offer Declined" 
  | "Application Withdrawn" | "Rejection Received" | "Feedback Requested" | "Feedback Received" 
  | "Networking Call" | "Informational Interview" | "Note Added";


// -------------- COMPANY TYPES --------------
export interface Company {
  id: number;
  name: string;
  foundation_date: string | null; // ISO date string
  industry: string | null;
  size: string | null;
  phase: CompanyPhase | null; 
  website: string | null; // HttpUrl maps to string
  linkedin: string | null; // HttpUrl maps to string
  crunchbase: string | null; // HttpUrl maps to string
  glassdoor: string | null; // HttpUrl maps to string
  short_description: string | null;
  notes: string | null;
  related_articles: string | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface CompanyCreate {
  name: string;
  foundation_date?: string | null;
  industry?: string | null;
  size?: string | null;
  phase?: CompanyPhase | null;
  website?: string | null;
  linkedin?: string | null;
  crunchbase?: string | null;
  glassdoor?: string | null;
  short_description?: string | null;
  notes?: string | null;
  related_articles?: string | null;
}

export interface CompanyUpdate extends Partial<Omit<Company, 'id' | 'created_at' | 'updated_at'>> {}


// -------------- JOB APPLICATION TYPES --------------
export interface JobApplication {
  id: number;
  company_id: number;
  title: string;
  description_text: string | null;
  job_url: string; // HttpUrl maps to string
  location_city: string | null;
  location_country: string | null;
  is_remote: boolean | null;
  employment_type: EmploymentType | null;
  used_resume: string | null;
  cover_letter_file_path: string | null;
  requested_salary_min: number | null;
  requested_salary_max: number | null;
  salary_currency: string | null;
  date_posted: string | null; // ISO date string
  status: ApplicationStatus;
  discovered_through_id: number;
  applied_through_text: string | null;
  referral: string | null;
  notes: string | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  // company?: Company; // Optional: for denormalized data if backend sends it
  // discovered_through_source?: JobSource; // Optional
}

export interface JobApplicationCreate {
  company_id: number;
  title: string;
  description_text?: string | null;
  job_url: string;
  location_city?: string | null;
  location_country?: string | null;
  is_remote?: boolean | null;
  employment_type?: EmploymentType | null;
  used_resume?: string | null;
  cover_letter_file_path?: string | null;
  requested_salary_min?: number | null;
  requested_salary_max?: number | null;
  salary_currency?: string | null;
  date_posted?: string | null;
  status?: ApplicationStatus; // Default is 'Considering' on backend
  discovered_through_id: number;
  applied_through_text?: string | null;
  referral?: string | null;
  notes?: string | null;
}

export interface JobApplicationUpdate extends Partial<Omit<JobApplication, 'id' | 'created_at' | 'updated_at' | 'company_id' | 'discovered_through_id'>> {
  // Generally, foreign keys like company_id and discovered_through_id might not be updatable or handled differently.
  // For now, making them updatable as per backend schema, but this can be refined.
  company_id?: number;
  title?: string;
  description_text?: string | null;
  job_url?: string;
  location_city?: string | null;
  location_country?: string | null;
  is_remote?: boolean | null;
  employment_type?: EmploymentType | null;
  used_resume?: string | null;
  cover_letter_file_path?: string | null;
  requested_salary_min?: number | null;
  requested_salary_max?: number | null;
  salary_currency?: string | null;
  date_posted?: string | null;
  status?: ApplicationStatus;
  discovered_through_id?: number;
  applied_through_text?: string | null;
  referral?: string | null;
  notes?: string | null;
}


// -------------- JOB SOURCE TYPES --------------
export interface JobSource {
  id: number;
  name: string;
  type: JobSourceType | null;
  website: string | null; // HttpUrl maps to string
  short_description: string | null;
  notes: string | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
}

export interface JobSourceCreate {
  name: string;
  type?: JobSourceType | null;
  website?: string | null;
  short_description?: string | null;
  notes?: string | null;
}

export interface JobSourceUpdate extends Partial<Omit<JobSource, 'id' | 'created_at' | 'updated_at'>> {}


// -------------- APPLICATION EVENT TYPES --------------
export interface ApplicationEvent {
  id: number;
  job_application_id: number; 
  event_type: ApplicationEventType;
  event_date: string; // ISO datetime string (default to now on backend)
  participants: string | null;
  notes: string | null;
  created_at: string; // ISO datetime string
  updated_at: string; // ISO datetime string
  // job_application?: JobApplication; // Optional, for denormalized data
}

export interface ApplicationEventCreate {
  job_application_id: number; 
  event_type: ApplicationEventType;
  event_date?: string; // Frontend might make it optional if backend defaults
  participants?: string | null;
  notes?: string | null;
}

export interface ApplicationEventUpdate extends Partial<Omit<ApplicationEvent, 'id' | 'created_at' | 'updated_at' | 'job_application_id'>> {
    // job_application_id is usually not updatable.
    event_type?: ApplicationEventType;
    event_date?: string;
    participants?: string | null;
    notes?: string | null;
}

// Generic type for API responses that might be paginated or structured
export interface ApiResponse<T> {
  data: T;
  // Add other potential API response fields like pagination info, success status, messages etc.
  // For now, keeping it simple.
} 