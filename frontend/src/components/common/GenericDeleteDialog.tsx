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
import { Button } from "@/components/ui/button";

interface GenericDeleteDialogProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  onConfirm: () => void;
  itemName: string; // e.g., "the company 'Tech Solutions Inc.'" or "this job application"
  itemType?: string; // e.g., "Company", "Job Application"
  title?: string;
  description?: string;
}

export default function GenericDeleteDialog({
  isOpen,
  onOpenChange,
  onConfirm,
  itemName,
  itemType = "item",
  title,
  description,
}: GenericDeleteDialogProps) {
  const dialogTitle = title || `Delete ${itemType}`;
  const dialogDescription = description || `Are you sure you want to delete ${itemName}? This action cannot be undone.`;

  const handleConfirm = () => {
    onConfirm();
    onOpenChange(false); // Close the dialog after confirmation
  };

  return (
    <AlertDialog open={isOpen} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>{dialogTitle}</AlertDialogTitle>
          <AlertDialogDescription>
            {dialogDescription}
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel asChild>
            <Button variant="outline">Cancel</Button>
          </AlertDialogCancel>
          <AlertDialogAction asChild>
            <Button variant="destructive" onClick={handleConfirm}>Delete</Button>
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
} 