import { JobApplication, JobApplicationCreate, JobApplicationUpdate } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const JOB_APPLICATIONS_ENDPOINT = `${API_BASE_URL}/api/v1/job-apps`;

export const fetchJobApplications = async (): Promise<JobApplication[]> => {
  const response = await fetch(`${JOB_APPLICATIONS_ENDPOINT}/`);
  if (!response.ok) {
    console.error('Fetch Job Applications - Response not OK. Status:', response.status, 'StatusText:', response.statusText);
    const errorText = await response.text();
    console.error('Fetch Job Applications - Raw error response:', errorText);
    let errorData = { detail: `Failed to fetch job applications. Status: ${response.status}` };
    try {
      errorData = JSON.parse(errorText);
    } catch (e) {
      console.error('Fetch Job Applications - Could not parse error response as JSON.');
    }
    console.error('Error fetching job applications:', errorData);
    throw new Error(errorData.detail || `Failed to fetch job applications. Status: ${response.status}`);
  }
  return response.json();
};

export const addJobApplication = async (jobApplicationData: JobApplicationCreate): Promise<JobApplication> => {
  const response = await fetch(`${JOB_APPLICATIONS_ENDPOINT}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jobApplicationData),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to add job application and could not parse error response.' }));
    console.error('Error adding job application:', errorData);
    throw new Error(errorData.detail || 'Failed to add job application');
  }
  return response.json();
};

export const updateJobApplication = async (id: number, jobApplicationData: JobApplicationUpdate): Promise<JobApplication> => {
  const response = await fetch(`${JOB_APPLICATIONS_ENDPOINT}/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jobApplicationData),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to update job application and could not parse error response.' }));
    console.error('Error updating job application:', errorData);
    throw new Error(errorData.detail || 'Failed to update job application');
  }
  return response.json();
};

export const deleteJobApplication = async (id: number): Promise<void> => {
  const response = await fetch(`${JOB_APPLICATIONS_ENDPOINT}/${id}/`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to delete job application and could not parse error response.' }));
    console.error('Error deleting job application:', errorData);
    throw new Error(errorData.detail || 'Failed to delete job application');
  }
  // No content expected for a successful delete
}; 