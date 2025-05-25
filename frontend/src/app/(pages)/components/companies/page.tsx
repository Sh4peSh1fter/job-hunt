"use client"; // Ensure this is a client component if using hooks like useState

import { useState, useEffect, useCallback } from 'react';
import { Button } from "@/components/ui/button";
import GenericDataTable, { ColumnConfig, DataItem } from "@/components/common/GenericDataTable";
import { GenericAddDialog, FormFieldConfig } from "@/components/common/GenericAddDialog";
import GenericViewDialog from "@/components/common/GenericViewDialog";
import GenericDeleteDialog from "@/components/common/GenericDeleteDialog";
import { Company, CompanyCreate, CompanyUpdate } from "@/lib/types";
import {
  fetchCompanies,
  addCompany,
  updateCompany,
  deleteCompany,
} from "@/lib/api/company-api";
import { PlusCircle } from 'lucide-react'; // Import PlusCircle

// Extend DataItem for Company specific usage if needed, though Company already has id
interface CompanyDataItem extends Company, DataItem {}

const companyColumnConfig: ColumnConfig<CompanyDataItem>[] = [
  { accessorKey: 'actions', header: 'Actions' }, // Placeholder for action buttons
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'name', header: 'Name', enableEdit: true, inputType: 'text' },
  { accessorKey: 'industry', header: 'Industry', enableEdit: true, inputType: 'text' },
  { accessorKey: 'website', header: 'Website', enableEdit: true, inputType: 'url' },
  { accessorKey: 'short_description', header: 'Short Description', enableEdit: true, inputType: 'textarea', minWidth: '250px' },
  { accessorKey: 'foundation_date', header: 'Foundation Date', enableEdit: true, inputType: 'date' },
  { accessorKey: 'size', header: 'Size', enableEdit: true, inputType: 'text' },
  { accessorKey: 'phase', header: 'Phase', enableEdit: true, inputType: 'select' /* We will add options later */ },
  { accessorKey: 'linkedin', header: 'LinkedIn', enableEdit: true, inputType: 'url' },
  { accessorKey: 'crunchbase', header: 'Crunchbase', enableEdit: true, inputType: 'url' },
  { accessorKey: 'glassdoor', header: 'Glassdoor', enableEdit: true, inputType: 'url' },
  { accessorKey: 'notes', header: 'Notes', enableEdit: true, inputType: 'textarea', minWidth: '250px' },
  { accessorKey: 'related_articles', header: 'Related Articles', enableEdit: true, inputType: 'textarea', minWidth: '250px' },
  { accessorKey: 'created_at', header: 'Created At' },
  { accessorKey: 'updated_at', header: 'Updated At' },
];

const companyFormFieldConfig: FormFieldConfig[] = [
  { name: 'name', label: 'Name', type: 'text', required: true },
  { name: 'industry', label: 'Industry', type: 'text' },
  { name: 'website', label: 'Website', type: 'url', placeholder: 'https://example.com' },
  { name: 'short_description', label: 'Short Description', type: 'textarea' },
  { name: 'foundation_date', label: 'Foundation Date', type: 'date' },
  { name: 'size', label: 'Size', type: 'text' },
  { name: 'phase', label: 'Phase', type: 'select', options: [
    {value: "Pre-Seed", label: "Pre-Seed"}, {value: "Seed", label: "Seed"}, {value: "Early", label: "Early"},
    {value: "Growth", label: "Growth"}, {value: "Expansion", label: "Expansion"}, {value: "Exit", label: "Exit"}
  ]}, // Example options
  { name: 'linkedin', label: 'LinkedIn', type: 'url', placeholder: 'https://linkedin.com/company/...' },
  { name: 'crunchbase', label: 'Crunchbase', type: 'url', placeholder: 'https://crunchbase.com/organization/...' },
  { name: 'glassdoor', label: 'Glassdoor', type: 'url', placeholder: 'https://glassdoor.com/Overview/Working-at-...' },
  { name: 'notes', label: 'Notes', type: 'textarea' },
  { name: 'related_articles', label: 'Related Articles (comma-separated URLs)', type: 'textarea' },
];

export default function CompaniesDataPage() {
  const [companies, setCompanies] = useState<CompanyDataItem[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  const [selectedCompany, setSelectedCompany] = useState<CompanyDataItem | null>(null);
  const [companyToUpdate, setCompanyToUpdate] = useState<Partial<CompanyCreate> | null>(null); // For add/edit

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      const data = await fetchCompanies();
      setCompanies(data as CompanyDataItem[]); // Cast if Company is compatible with CompanyDataItem
      setError(null);
    } catch (err: any) {      
      setError(err.message || "Failed to fetch companies.");
      setCompanies([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAddCompany = async (companyData: CompanyCreate) => {
    try {
      await addCompany(companyData);
      fetchData(); // Refetch data after adding
      // Optionally, show a success toast/message
    } catch (err: any) {
      console.error("Failed to add company:", err);
      setError(`Add Error: ${err.message}`); // Display error on the page or in a toast
      throw err; // Re-throw to keep the dialog open and show error there
    }
  };

  const handleUpdateCompany = async (editedData: Partial<CompanyDataItem>, originalCompany: CompanyDataItem) => {
    try {
      // Ensure id is not in editedData or use originalCompany.id
      const updatePayload: CompanyUpdate = { ...editedData };
      delete (updatePayload as any).id; // Ensure id is not part of the payload for update API
      delete (updatePayload as any).created_at;
      delete (updatePayload as any).updated_at;

      await updateCompany(originalCompany.id, updatePayload);
      fetchData(); // Refetch
      // Optionally, show a success toast/message
    } catch (err: any) {
      console.error("Failed to update company:", err);
      setError(`Update Error: ${err.message}`); 
      throw err; // Re-throw for GenericDataTable to catch
    }
  };

  const handleDeleteCompany = async (companyId: number) => {
    try {
      await deleteCompany(companyId);
      fetchData(); // Refetch
      setIsDeleteDialogOpen(false); // Close confirmation dialog
      setSelectedCompany(null);
      // Optionally, show a success toast/message
    } catch (err: any) {
      console.error("Failed to delete company:", err);
      setError(`Delete Error: ${err.message}`);
      // Dialog might still close, error displayed on page
    }
  };

  // Action handlers for GenericDataTable
  const handleViewAction = (item: CompanyDataItem) => {
    setSelectedCompany(item);
    setIsViewDialogOpen(true);
  };

  const handleDeleteAction = (item: CompanyDataItem) => {
    setSelectedCompany(item);
    setIsDeleteDialogOpen(true);
  };

  // The GenericDataTable will internally handle the onEdit and onSaveEdit toggle for its inputs.
  // The onSaveEdit prop passed to it will be our handleUpdateCompany.

  return (
    <div className="container mx-auto py-6">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-semibold">Companies</h1>
        <Button onClick={() => { setCompanyToUpdate(null); setIsAddDialogOpen(true); }}>
          <PlusCircle className="mr-2 h-4 w-4" />
          Add New Company
        </Button>
      </div>

      {error && <p className="text-red-500 bg-red-100 p-3 rounded-md mb-4">Error: {error}</p>}

      <GenericDataTable<CompanyDataItem>
        data={companies}
        columns={companyColumnConfig}        
        isLoading={isLoading}
        error={null} // Page level error is handled above, table can have its own internal errors for actions
        onView={handleViewAction}
        onSaveEdit={handleUpdateCompany} // Pass the update handler
        onDelete={handleDeleteAction} // Pass the delete handler
        // onEdit is handled internally by GenericDataTable to toggle its state
      />

      <GenericAddDialog<CompanyCreate>
        isOpen={isAddDialogOpen}
        onOpenChange={setIsAddDialogOpen}
        onSave={handleAddCompany}
        formFields={companyFormFieldConfig}
        itemType="Company"
        initialState={companyToUpdate || {}} // Pass null or existing data for editing (if we merge Add/Edit)
      />

      {selectedCompany && (
        <GenericViewDialog
          isOpen={isViewDialogOpen}
          onOpenChange={setIsViewDialogOpen}
          item={selectedCompany}
          itemType="Company"
          excludedKeys={['created_at', 'updated_at']} // Example: hide timestamps in view
        />
      )}

      {selectedCompany && (
        <GenericDeleteDialog
          isOpen={isDeleteDialogOpen}
          onOpenChange={setIsDeleteDialogOpen}
          onConfirm={() => handleDeleteCompany(selectedCompany.id)}
          itemName={`company "${selectedCompany.name}"`}
          itemType="Company"
        />
      )}
    </div>
  );
} 