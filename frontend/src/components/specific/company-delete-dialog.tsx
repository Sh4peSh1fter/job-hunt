"use client";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";

interface Company {
  id: number;
  name: string;
  // Add other fields if needed for display in the confirmation, though usually just name is enough
}

interface CompanyDeleteDialogProps {
  company: Company | null;
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  onConfirmDelete: (companyId: number) => void;
}

export default function CompanyDeleteDialog(
  { company, isOpen, onOpenChange, onConfirmDelete }: CompanyDeleteDialogProps
) {
  if (!company) {
    return null;
  }

  const handleConfirm = () => {
    onConfirmDelete(company.id);
    onOpenChange(false); // Close dialog after confirmation
  };

  return (
    <AlertDialog open={isOpen} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Are you absolutely sure?</AlertDialogTitle>
          <AlertDialogDescription>
            This action cannot be undone. This will permanently delete the company "<strong>{company.name}</strong>" (ID: {company.id}) and all associated data.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel onClick={() => onOpenChange(false)}>Cancel</AlertDialogCancel>
          <AlertDialogAction onClick={handleConfirm} className="bg-red-600 hover:bg-red-700">
            Delete
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
} 