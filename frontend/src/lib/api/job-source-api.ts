import { JobSource, JobSourceCreate, JobSourceUpdate } from '@/lib/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
const JOB_SOURCES_ENDPOINT = `${API_BASE_URL}/api/v1/job-srcs`;

export const fetchJobSources = async (): Promise<JobSource[]> => {
  const response = await fetch(`${JOB_SOURCES_ENDPOINT}/`);
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to fetch job sources and could not parse error response.' }));
    console.error('Error fetching job sources:', errorData);
    throw new Error(errorData.detail || 'Failed to fetch job sources');
  }
  return response.json();
};

export const addJobSource = async (jobSourceData: JobSourceCreate): Promise<JobSource> => {
  const response = await fetch(`${JOB_SOURCES_ENDPOINT}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jobSourceData),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to add job source and could not parse error response.' }));
    console.error('Error adding job source:', errorData);
    throw new Error(errorData.detail || 'Failed to add job source');
  }
  return response.json();
};

export const updateJobSource = async (id: number, jobSourceData: JobSourceUpdate): Promise<JobSource> => {
  const response = await fetch(`${JOB_SOURCES_ENDPOINT}/${id}/`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(jobSourceData),
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to update job source and could not parse error response.' }));
    console.error('Error updating job source:', errorData);
    throw new Error(errorData.detail || 'Failed to update job source');
  }
  return response.json();
};

export const deleteJobSource = async (id: number): Promise<void> => {
  const response = await fetch(`${JOB_SOURCES_ENDPOINT}/${id}/`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Failed to delete job source and could not parse error response.' }));
    console.error('Error deleting job source:', errorData);
    throw new Error(errorData.detail || 'Failed to delete job source');
  }
  // No content expected for a successful delete
}; 