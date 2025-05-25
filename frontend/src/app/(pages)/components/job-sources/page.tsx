'use client';

import React from 'react';
import GenericDataTable, { ColumnConfig } from '@/components/common/GenericDataTable';
import { GenericAddDialog, FormFieldConfig } from '@/components/common/GenericAddDialog';
import GenericViewDialog from '@/components/common/GenericViewDialog';
import GenericDeleteDialog from '@/components/common/GenericDeleteDialog';
import { Button } from '@/components/ui/button';
import { PlusCircle } from 'lucide-react';
import { JobSource, JobSourceCreate, JobSourceUpdate, JobSourceType } from '@/lib/types';
import {
  fetchJobSources,
  addJobSource,
  updateJobSource,
  deleteJobSource,
} from '@/lib/api/job-source-api';

const jobSourceColumns: ColumnConfig<JobSource>[] = [
  { accessorKey: 'actions', header: 'Actions' },
  { accessorKey: 'id', header: 'ID' },
  { accessorKey: 'name', header: 'Name', enableEdit: true, inputType: 'text' },
  {
    accessorKey: 'type',
    header: 'Type',
    cellContent: (item) => item.type ? item.type : 'N/A',
    enableEdit: true,
    inputType: 'select',
    options: ['Job Board', 'Recruiter', 'Company Website', 'Networking', 'Referral Program', 'Other'].map(t => ({ value: t, label: t })),
  },
  {
    accessorKey: 'website',
    header: 'Website',
    cellContent: (item) => item.website ? <a href={item.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Link</a> : 'N/A',
    enableEdit: true,
    inputType: 'url',
  },
  { 
    accessorKey: 'short_description', 
    header: 'Description',
    cellContent: (item) => item.short_description || 'N/A',
    enableEdit: true,
    inputType: 'textarea',
  },
  { 
    accessorKey: 'notes', 
    header: 'Notes',
    cellContent: (item) => item.notes || 'N/A',
    enableEdit: true,
    inputType: 'textarea',
  },
  {
    accessorKey: 'created_at',
    header: 'Created At',
    cellContent: (item) => item.created_at ? new Date(item.created_at).toLocaleDateString() : 'N/A',
  },
  {
    accessorKey: 'updated_at',
    header: 'Updated At',
    cellContent: (item) => item.updated_at ? new Date(item.updated_at).toLocaleDateString() : 'N/A',
  },
];

const jobSourceFormFields: FormFieldConfig[] = [
  { name: 'name', label: 'Name', type: 'text', required: true },
  {
    name: 'type',
    label: 'Type',
    type: 'select',
    options: ['Job Board', 'Recruiter', 'Company Website', 'Networking', 'Referral Program', 'Other'].map(t => ({ value: t, label: t })),
  },
  { name: 'website', label: 'Website', type: 'url' },
  { name: 'short_description', label: 'Short Description', type: 'textarea' }, 
  { name: 'notes', label: 'Notes', type: 'textarea' },
];

const ALL_JOB_SOURCE_TYPES_FOR_PAGE: JobSourceType[] = ["Job Board", "Recruiter", "Company Website", "Networking", "Referral Program", "Other"];

export default function JobSourcesPage() {
  const [data, setData] = React.useState<JobSource[]>([]);
  const [isLoading, setIsLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  const [isAddDialogOpen, setIsAddDialogOpen] = React.useState(false);
  const [editingItem, setEditingItem] = React.useState<JobSource | null>(null);
  const [viewingItem, setViewingItem] = React.useState<JobSource | null>(null);
  const [deletingItemId, setDeletingItemId] = React.useState<number | null>(null);

  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const jobSources = await fetchJobSources();
      setData(jobSources);
    } catch (err: any) {      
      setError(err.message || 'Failed to fetch job sources');
      console.error("Error fetching data:", err.message || 'An unexpected error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    loadData();
  }, []);

  const handleAddOrUpdate = async (itemData: JobSourceCreate | JobSourceUpdate) => {
    try {
      if (editingItem && editingItem.id) { // Update
        await updateJobSource(editingItem.id, itemData as JobSourceUpdate);
        console.log("Job Source updated successfully!");
      } else { // Add
        await addJobSource(itemData as JobSourceCreate);
        console.log("Job Source added successfully!");
      }
      loadData(); 
      setIsAddDialogOpen(false);
      setEditingItem(null);
    } catch (err: any) {
      const action = editingItem ? 'updating' : 'adding';
      console.error(`Failed to ${action} job source:`, err);
      console.error(`Error ${action} item:`, err.message || `Could not ${action} job source.`);
      // Consider setting an error state to display in the dialog itself
    }
  };
  
  const openAddDialog = () => {
    setEditingItem(null);
    setIsAddDialogOpen(true);
  };

  const openEditDialog = (item: JobSource) => {
    setEditingItem(item);
    setIsAddDialogOpen(true); 
  };

  const handleDeleteConfirm = async () => {
    if (deletingItemId === null) return;
    try {
      await deleteJobSource(deletingItemId);
      loadData();
      console.log("Job Source deleted successfully!");
    } catch (err: any) {
      console.error('Failed to delete job source:', err);
      console.error("Error deleting item:", err.message || 'Could not delete job source.');
    } finally {
      setDeletingItemId(null);
    }
  };

  const memoizedInitialState = React.useMemo(() => {
    const newInitialState: Partial<JobSourceCreate & JobSourceUpdate> = {};
    
    if (editingItem) {
      // Populate from editingItem
      jobSourceFormFields.forEach(field => {
        const key = field.name as keyof JobSource;
        const editKey = field.name as keyof JobSourceUpdate;
        if (field.name === 'type') {
          const currentType = editingItem.type;
          newInitialState.type = ALL_JOB_SOURCE_TYPES_FOR_PAGE.includes(currentType as JobSourceType) 
                                   ? currentType as JobSourceType 
                                   : undefined;
        } else {
          // For other fields, directly assign if present, otherwise use default based on type
          newInitialState[editKey] = editingItem[key] !== undefined && editingItem[key] !== null 
                                      ? editingItem[key] 
                                      : (field.type === 'number' ? null : '');
        }
      });
    } else {
      // Defaults for adding a new item
      jobSourceFormFields.forEach(field => {
        const createKey = field.name as keyof JobSourceCreate;
        if (field.name === 'type') {
          newInitialState.type = undefined;
        } else {
          newInitialState[createKey] = field.type === 'number' ? null : '';
        }
      });
      // Ensure 'name' has a default if not covered (though it should be)
      if (newInitialState.name === undefined) newInitialState.name = '';
    }
    return newInitialState;
  }, [editingItem]);

  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Job Sources</h1>
        <Button onClick={openAddDialog}>
          <PlusCircle className="mr-2 h-4 w-4" /> Add New Job Source
        </Button>
      </div>

      {error && <p className="text-red-500 bg-red-100 p-3 rounded-md">Error: {error}</p>}

      <GenericDataTable<JobSource>        
        columns={jobSourceColumns}
        data={data}
        isLoading={isLoading}
        itemType="Job Source"
        onView={(item: JobSource) => setViewingItem(item)}
        onSaveEdit={async (updatedData, originalData) => {
          await handleAddOrUpdate({ ...originalData, ...updatedData }); 
        }}
        onDelete={(item: JobSource) => setDeletingItemId(item.id)}
        error={error}
      />

      {isAddDialogOpen && (
        <GenericAddDialog<Partial<JobSourceCreate & JobSourceUpdate>>
          isOpen={isAddDialogOpen}
          onOpenChange={setIsAddDialogOpen}
          onSave={handleAddOrUpdate}
          formFields={jobSourceFormFields}
          itemType="Job Source"
          initialState={memoizedInitialState}
          title={editingItem ? "Edit Job Source" : "Add New Job Source"}
        />
      )}

      {viewingItem && (
        <GenericViewDialog
          isOpen={!!viewingItem}
          onOpenChange={(isOpen) => !isOpen && setViewingItem(null)}
          item={viewingItem}
          itemType="Job Source"
          excludedKeys={['id', 'created_at', 'updated_at']}
        />
      )}

      {deletingItemId !== null && (
        <GenericDeleteDialog
          isOpen={deletingItemId !== null}
          onOpenChange={(isOpen) => !isOpen && setDeletingItemId(null)}
          onConfirm={handleDeleteConfirm}
          itemName={data.find((item: JobSource) => item.id === deletingItemId)?.name || "the selected item"}
          itemType="Job Source"
        />
      )}
    </div>
  );
} 