import { Company, CompanyCreate, CompanyUpdate } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

/**
 * Fetches all companies from the backend.
 * @returns A promise that resolves to an array of Company objects.
 */
export async function fetchCompanies(): Promise<Company[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/companies/`);
    if (!response.ok) {
      const errorText = await response.text();
      console.error("API Error - fetchCompanies - Response Text:", errorText);
      throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch companies:", error);
    // In a real app, you might throw a more specific error or handle it differently
    throw error; 
  }
}

/**
 * Adds a new company to the backend.
 * @param companyData - The data for the new company.
 * @returns A promise that resolves to the newly created Company object.
 */
export async function addCompany(companyData: CompanyCreate): Promise<Company> {
  try {
    const response = await fetch(`${API_BASE_URL}/companies/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(companyData),
    });
    if (!response.ok) {
      // Attempt to parse error details for better messages
      let errorMessage = 'Failed to add company';
      try {
        const errorData = await response.json();
        if (errorData.detail) {
          if (typeof errorData.detail === 'string') {
            errorMessage = errorData.detail;
          } else if (Array.isArray(errorData.detail)) {
            errorMessage = errorData.detail.map((err: any) => `${err.loc.join(' -> ')}: ${err.msg}`).join('; ');
          } else {
            errorMessage = JSON.stringify(errorData.detail);
          }
        }
      } catch (jsonError) {
        errorMessage = response.statusText || 'Server error during add company.';
      }
      console.error("API Error - addCompany:", errorMessage);
      throw new Error(errorMessage);
    }
    return await response.json();
  } catch (error) {
    console.error("Error adding company:", error);
    throw error;
  }
}

/**
 * Updates an existing company on the backend.
 * @param id - The ID of the company to update.
 * @param companyData - The data to update the company with.
 * @returns A promise that resolves to the updated Company object.
 */
export async function updateCompany(id: number, companyData: CompanyUpdate): Promise<Company> {
  try {
    const response = await fetch(`${API_BASE_URL}/companies/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(companyData),
    });
    if (!response.ok) {
      const errorText = await response.text(); // Or parse JSON if backend sends detailed errors
      console.error("API Error - updateCompany - Response Text:", errorText);
      throw new Error(`Failed to update company: ${errorText}`);
    }
    return await response.json();
  } catch (error) {
    console.error("Error updating company:", error);
    throw error;
  }
}

/**
 * Deletes a company from the backend.
 * @param id - The ID of the company to delete.
 * @returns A promise that resolves to true if deletion was successful, false otherwise (or throws an error).
 */
export async function deleteCompany(id: number): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/companies/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      // Check for specific status codes if needed, e.g., 204 No Content for successful delete
      // For now, any non-ok status is an error.
      const errorText = await response.text();
      console.error("API Error - deleteCompany - Response Text:", errorText);
      throw new Error(`Failed to delete company: ${errorText}`);
    }
    // If backend returns 204 No Content, response.json() will fail.
    // So, for DELETE, success is often indicated by a 200, 202, or 204 status.
    return response.status === 200 || response.status === 204 || response.status === 202; 
  } catch (error) {
    console.error("Error deleting company:", error);
    throw error;
  }
} 