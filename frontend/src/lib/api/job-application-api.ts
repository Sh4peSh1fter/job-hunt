import { JobApplication, JobApplicationCreate, JobApplicationUpdate } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';

export const fetchJobApplications = async (): Promise<JobApplication[]> => {
  const response = await fetch(`${API_BASE_URL}/api/v1/job-applications/`);
  if (!response.ok) {
    console.error('Fetch Job Applications - Response not OK. Status:', response.status, 'StatusText:', response.statusText);
    const errorText = await response.text(); // Get raw text to see what the server is actually sending
    console.error('Fetch Job Applications - Raw error response:', errorText);
    let errorData = { detail: `Failed to fetch job applications. Status: ${response.status}` };
    try {
      errorData = JSON.parse(errorText); // Try to parse it as JSON
    } catch (e) {
      console.error('Fetch Job Applications - Could not parse error response as JSON.');
      // errorData.detail is already set as a fallback
    }
    console.error('Error fetching job applications:', errorData);
    throw new Error(errorData.detail || `Failed to fetch job applications. Status: ${response.status}`);
  }
  return response.json();
};

export const addJobApplication = async (jobApplicationData: JobApplicationCreate): Promise<JobApplication> => {
  const response = await fetch(`${API_BASE_URL}/api/v1/job-applications/`, {
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
  const response = await fetch(`${API_BASE_URL}/api/v1/job-applications/${id}/`, {
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
  const response = await fetch(`${API_BASE_URL}/api/v1/job-applications/${id}/`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to delete job application and could not parse error response.' }));
    console.error('Error deleting job application:', errorData);
    throw new Error(errorData.detail || 'Failed to delete job application');
  }
  // No content expected for a successful delete
}; 