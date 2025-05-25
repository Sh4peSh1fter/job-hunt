"use client";

import { useState, useEffect, useCallback } from 'react';
import { PlusCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import GenericDataTable, { ColumnConfig, DataItem } from '@/components/common/GenericDataTable';
import { GenericAddDialog, FormFieldConfig } from '@/components/common/GenericAddDialog';
import GenericViewDialog from '@/components/common/GenericViewDialog';
import GenericDeleteDialog from '@/components/common/GenericDeleteDialog';
import {
  JobApplication,
  JobApplicationCreate,
  JobApplicationUpdate,
  ApplicationStatus,
  Company,
  JobSource,
  EmploymentType,
} from '@/lib/types'; // Added EmploymentType
import {
  fetchJobApplications,
  addJobApplication,
  updateJobApplication,
  deleteJobApplication,
} from '@/lib/api/job-application-api';
import { fetchCompanies } from '@/lib/api/company-api';
import { fetchJobSources } from '@/lib/api/job-source-api';
import React from 'react';

// Extend DataItem for JobApplication specific usage
interface JobApplicationDataItem extends JobApplication, DataItem {}

const ALL_APPLICATION_STATUSES: ApplicationStatus[] = [
  "Considering", "Not Pursuing", "Applied", "In Progress", 
  "Withdrawn", "Offered", "Rejected", "Expired"
];

const ALL_EMPLOYMENT_TYPES: EmploymentType[] = [
  "Full-time", "Part-time", "Contract", "Internship", "Temporary", "Volunteer"
];

const JobApplicationsPage = () => {
  const [jobApplications, setJobApplications] = useState<JobApplicationDataItem[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [jobSources, setJobSources] = useState<JobSource[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [selectedJobApplication, setSelectedJobApplication] = useState<JobApplicationDataItem | null>(null);
  // No need for companyToUpdate if GenericAddDialog handles its own fresh state for additions

  const loadData = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const [appsData, companiesData, sourcesData] = await Promise.all([
        fetchJobApplications(),
        fetchCompanies(),
        fetchJobSources(),
      ]);
      setJobApplications(appsData as JobApplicationDataItem[]);
      setCompanies(companiesData);
      setJobSources(sourcesData);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch data.');
      console.error(err);
      setJobApplications([]); // Clear data on error
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAddJobApplication = async (data: JobApplicationCreate) => {
    try {
        const payload: JobApplicationCreate = {
            ...data,
            company_id: Number(data.company_id),
            discovered_through_id: Number(data.discovered_through_id),
            date_posted: data.date_posted ? new Date(data.date_posted).toISOString().split('T')[0] : null, // Format as YYYY-MM-DD
            status: data.status || "Applied", // Ensure status has a default
            is_remote: data.is_remote === undefined ? null : Boolean(data.is_remote), // Handle boolean conversion
            requested_salary_min: data.requested_salary_min ? Number(data.requested_salary_min) : null,
            requested_salary_max: data.requested_salary_max ? Number(data.requested_salary_max) : null,
        };
        await addJobApplication(payload);
        loadData();
    } catch (err:any) {
        console.error("Failed to add job application:", err);
        setError(`Add Error: ${err.message}`);
        throw err; // Re-throw for GenericAddDialog to catch
    }
  };

  const handleUpdateJobApplication = async (data: Partial<JobApplicationUpdate>, originalItem: JobApplicationDataItem) => {
    try {
        const payload: JobApplicationUpdate = {
            ...data,
            company_id: data.company_id ? Number(data.company_id) : undefined,
            discovered_through_id: data.discovered_through_id ? Number(data.discovered_through_id) : undefined,
            date_posted: data.date_posted ? new Date(data.date_posted).toISOString().split('T')[0] : (data.date_posted === '' ? null : undefined),
            is_remote: data.is_remote === undefined ? undefined : Boolean(data.is_remote),
            requested_salary_min: data.requested_salary_min ? Number(data.requested_salary_min) : (data.requested_salary_min === null ? null : undefined),
            requested_salary_max: data.requested_salary_max ? Number(data.requested_salary_max) : (data.requested_salary_max === null ? null : undefined),
        };
        await updateJobApplication(originalItem.id, payload);
        loadData();
    } catch (err: any) {
        console.error("Failed to update job application:", err);
        setError(`Update Error: ${err.message}`);
        throw err; // Re-throw for GenericDataTable to catch
    }
  };

  const handleDeleteJobApplication = async (id: number) => {
    try {
        await deleteJobApplication(id);
        loadData();
        setIsDeleteDialogOpen(false);
        setSelectedJobApplication(null);
    } catch (err: any) {
        console.error("Failed to delete job application:", err);
        setError(`Delete Error: ${err.message}`);
    }
  };

  const handleViewAction = (item: JobApplicationDataItem) => {
    setSelectedJobApplication(item);
    setIsViewDialogOpen(true);
  };

  const handleDeleteAction = (item: JobApplicationDataItem) => {
    setSelectedJobApplication(item);
    setIsDeleteDialogOpen(true);
  };

  const jobApplicationColumnConfig: ColumnConfig<JobApplicationDataItem>[] = React.useMemo(() => [
    { accessorKey: 'actions', header: 'Actions' },
    { accessorKey: 'id', header: 'ID' },
    { accessorKey: 'title', header: 'Job Title', enableEdit: true, inputType: 'text' },
    {
      accessorKey: 'company_id',
      header: 'Company',
      cellContent: (item: JobApplicationDataItem) => companies.find(c => c.id === item.company_id)?.name || 'N/A',
      options: companies.map(c => ({ value: String(c.id), label: c.name })),
      enableEdit: true, inputType: 'select',
      formFieldConfig: { name: 'company_id', label: 'Company', type: 'select', required: true, options: companies.map(c => ({ value: String(c.id), label: c.name }))}
    },
    { accessorKey: 'job_url', header: 'Link', inputType: 'url', cellContent: (item: JobApplicationDataItem) => item.job_url ? <a href={item.job_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Link</a> : 'N/A', enableEdit: true }, 
    { accessorKey: 'date_posted', header: 'Date Posted', enableEdit: true, inputType: 'date' },
    {
      accessorKey: 'status',
      header: 'Status',
      options: ALL_APPLICATION_STATUSES.map(s => ({ value: s, label: s })),
      enableEdit: true, inputType: 'select',
      formFieldConfig: { name: 'status', label: 'Status', type: 'select', required: true, options: ALL_APPLICATION_STATUSES.map(s => ({ value: s, label: s }))}
    },
    {
      accessorKey: 'discovered_through_id',
      header: 'Source',
      cellContent: (item: JobApplicationDataItem) => jobSources.find(js => js.id === item.discovered_through_id)?.name || 'N/A',
      options: jobSources.map(js => ({ value: String(js.id), label: js.name })),
      enableEdit: true, inputType: 'select',
      formFieldConfig: { name: 'discovered_through_id', label: 'Job Source', type: 'select', required: true, options: jobSources.map(js => ({ value: String(js.id), label: js.name }))}
    },
    // Add more columns as needed, e.g., location, is_remote, etc.
    { accessorKey: 'notes', header: 'Notes', enableEdit: true, inputType: 'textarea', minWidth: '200px' },
  ], [companies, jobSources]);

  const jobApplicationFormFieldConfig: FormFieldConfig[] = React.useMemo(() => [
    { name: 'title', label: 'Job Title', type: 'text', required: true, placeholder: 'e.g., Software Engineer' },
    {
      name: 'company_id',
      label: 'Company',
      type: 'select',
      required: true,
      options: companies.map(c => ({ value: String(c.id), label: c.name })),
      placeholder: 'Select Company'
    },
    {
      name: 'discovered_through_id',
      label: 'Job Source',
      type: 'select',
      required: true,
      options: jobSources.map(js => ({ value: String(js.id), label: js.name })),
      placeholder: 'Select Job Source'
    },
    { name: 'job_url', label: 'Job URL', type: 'url', required: true, placeholder: 'https://example.com/job/123' },
    { name: 'date_posted', label: 'Date Posted', type: 'date' },
    {
      name: 'status',
      label: 'Status',
      type: 'select',
      required: true,
      options: ALL_APPLICATION_STATUSES.map(s => ({ value: s, label: s })),
      defaultValue: "Applied"
    },
    { name: 'description_text', label: 'Description', type: 'textarea', placeholder: 'Paste job description here...' },
    { name: 'location_city', label: 'City', type: 'text', placeholder: 'e.g., San Francisco' },
    { name: 'location_country', label: 'Country', type: 'text', placeholder: 'e.g., USA' },
    { name: 'is_remote', label: 'Remote?', type: 'select', options: [{value: "true", label: "Yes"}, {value: "false", label: "No"}, {value: "", label: "N/A"}], defaultValue: "" },
    { name: 'employment_type', label: 'Employment Type', type: 'select', options: ALL_EMPLOYMENT_TYPES.map(t => ({value: t, label: t})), placeholder: 'Select Type' },
    { name: 'used_resume', label: 'Resume Used', type: 'text', placeholder: 'e.g., General Tech Resume v3' },
    { name: 'cover_letter_file_path', label: 'Cover Letter Path', type: 'text', placeholder: 'e.g., /path/to/cover_letter.pdf' }, 
    { name: 'requested_salary_min', label: 'Min Salary Req.', type: 'number', placeholder: 'e.g., 80000' },
    { name: 'requested_salary_max', label: 'Max Salary Req.', type: 'number', placeholder: 'e.g., 120000' },
    { name: 'salary_currency', label: 'Salary Currency', type: 'text', placeholder: 'e.g., USD' },
    { name: 'applied_through_text', label: 'Applied Via', type: 'text', placeholder: 'e.g., LinkedIn Easy Apply, Company Portal' },
    { name: 'referral', label: 'Referral', type: 'text', placeholder: 'Name of referrer or N/A' },
    { name: 'notes', label: 'Notes', type: 'textarea', placeholder: 'Any notes about this application...' },
  ], [companies, jobSources]);

  return (
    <div className="container mx-auto py-4 px-0 md:px-4">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-semibold">Job Applications</h1>
        <Button onClick={() => setIsAddDialogOpen(true)}>
          <PlusCircle className="mr-2 h-4 w-4" /> Add New Job Application
        </Button>
      </div>

      {error && <p className="text-red-500 bg-red-100 p-3 rounded-md mb-4">Error: {error}</p>}

      <GenericDataTable<JobApplicationDataItem>
        columns={jobApplicationColumnConfig}
        data={jobApplications}
        isLoading={isLoading}
        error={null} // Page level error is handled above
        onView={handleViewAction}
        onSaveEdit={handleUpdateJobApplication}
        onDelete={handleDeleteAction}
        itemType="Job Application" // For messages within GenericDataTable if needed
      />

      <GenericAddDialog<JobApplicationCreate>
        isOpen={isAddDialogOpen}
        onOpenChange={setIsAddDialogOpen}
        onSave={handleAddJobApplication}
        formFields={jobApplicationFormFieldConfig}
        itemType="Job Application"
        title="Add New Job Application"
        // initialState can be used if opening the dialog for editing an existing item, but for add, it's {} by default
      />

      {selectedJobApplication && (
        <GenericViewDialog
          isOpen={isViewDialogOpen}
          onOpenChange={setIsViewDialogOpen}
          item={selectedJobApplication}
          itemType="Job Application"
          // Provide specific fields to display or a custom render function if needed
          // For now, it will display all item properties not in excludedKeys
          excludedKeys={['id', 'created_at', 'updated_at', 'company_id', 'discovered_through_id']} // Example
          // You might want to map company_id to company name, etc. here or in GenericViewDialog
        />
      )}

      {selectedJobApplication && (
        <GenericDeleteDialog
          isOpen={isDeleteDialogOpen}
          onOpenChange={setIsDeleteDialogOpen}
          onConfirm={() => handleDeleteJobApplication(selectedJobApplication.id)}
          itemName={selectedJobApplication.title || `Application ID: ${selectedJobApplication.id}`}
          itemType="Job Application"
        />
      )}
    </div>
  );
};

export default JobApplicationsPage;
