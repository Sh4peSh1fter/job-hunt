"use client";

import { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { CompanyCreate } from '@/lib/types'; // Import centralized type
import { addCompany } from '@/lib/api/company-api'; // Import API function

// Base Company type for creation (ID, created_at, updated_at are handled by backend)
// interface CompanyCreate { ... } // This is now imported

interface CompanyAddDialogProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  onCompanyAdded: () => void; // Callback to refresh the table
}

const initialFormState: CompanyCreate = {
  name: '',
  foundation_date: null,
  industry: null,
  size: null,
  phase: null,
  website: null,
  linkedin: null,
  crunchbase: null,
  glassdoor: null,
  short_description: null,
  notes: null,
  related_articles: null,
};

export default function CompanyAddDialog({ isOpen, onOpenChange, onCompanyAdded }: CompanyAddDialogProps) {
  const [formData, setFormData] = useState<CompanyCreate>(initialFormState);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Reset form when dialog opens/closes if it's not just being closed after save
    if (isOpen) {
      setFormData(initialFormState);
      setError(null);
      setIsSaving(false);
    }
  }, [isOpen]);

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = event.target;
    setFormData(prevData => ({
      ...prevData,
      [name]: value === '' ? null : value,
    }));
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setIsSaving(true);
    setError(null);

    if (!formData.name) {
        setError("Company name is required.");
        setIsSaving(false);
        return;
    }

    const payload = { ...formData }; // Create a mutable copy

    // Explicitly handle HttpUrl fields
    const urlFieldKeys: (keyof Pick<CompanyCreate, 'website' | 'linkedin' | 'crunchbase' | 'glassdoor'>)[] = [
      'website', 
      'linkedin', 
      'crunchbase', 
      'glassdoor'
    ];

    for (const key of urlFieldKeys) {
      if (payload[key] === '') {
        payload[key] = null;
      }
    }

    try {
      // const response = await fetch('http://localhost:8000/api/v1/companies/', { ... }); // Old fetch
      await addCompany(payload); // Use the new API function
      
      // if (!response.ok) { ... } // Old error handling, now done in addCompany
      // throw new Error(errorMessage);
      
      onCompanyAdded(); // Trigger table refresh
      onOpenChange(false); // Close dialog

    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred.');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] p-6 flex flex-col max-h-[90vh]">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle>Add New Company</DialogTitle>
          <DialogDescription>
            Fill in the details below to add a new company to your records.
          </DialogDescription>
        </DialogHeader>
        <form onSubmit={handleSubmit} id="company-add-form" className="grid gap-4 overflow-y-auto flex-grow py-4 pr-2">
          <p className="text-red-600 text-sm min-h-[1.25rem]">{error ? `Error: ${error}` : <>&nbsp;</>}</p>
          
          {/* Name Field */}
          <div>
            <Label htmlFor="name">Name*</Label>
            <Input id="name" name="name" value={formData.name} onChange={handleInputChange} className="mt-1" required />
          </div>
          {/* Industry Field */}
          <div>
            <Label htmlFor="industry">Industry</Label>
            <Input id="industry" name="industry" value={formData.industry || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Website Field */}
          <div>
            <Label htmlFor="website">Website</Label>
            <Input id="website" name="website" value={formData.website || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Short Description Field */}
          <div>
            <Label htmlFor="short_description">Short Description</Label>
            <Input id="short_description" name="short_description" value={formData.short_description || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Foundation Date Field */}
          <div>
            <Label htmlFor="foundation_date">Foundation Date</Label>
            <Input id="foundation_date" name="foundation_date" type="date" value={formData.foundation_date || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Size Field */}
          <div>
            <Label htmlFor="size">Size</Label>
            <Input id="size" name="size" value={formData.size || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Phase Field */}
          <div>
            <Label htmlFor="phase">Phase</Label>
            <Input id="phase" name="phase" value={formData.phase || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* LinkedIn Field */}
          <div>
            <Label htmlFor="linkedin">LinkedIn</Label>
            <Input id="linkedin" name="linkedin" value={formData.linkedin || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Crunchbase Field */}
          <div>
            <Label htmlFor="crunchbase">Crunchbase</Label>
            <Input id="crunchbase" name="crunchbase" value={formData.crunchbase || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Glassdoor Field */}
          <div>
            <Label htmlFor="glassdoor">Glassdoor</Label>
            <Input id="glassdoor" name="glassdoor" value={formData.glassdoor || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Notes Field */}
          <div>
            <Label htmlFor="notes">Notes</Label>
            <Input id="notes" name="notes" value={formData.notes || ''} onChange={handleInputChange} className="mt-1" />
          </div>
          {/* Related Articles Field */}
          <div>
            <Label htmlFor="related_articles">Related Articles</Label>
            <Input id="related_articles" name="related_articles" value={formData.related_articles || ''} onChange={handleInputChange} className="mt-1" />
          </div>

        </form>
        <DialogFooter className="flex-shrink-0 pt-4">
          <DialogClose asChild>
            <Button type="button" variant="outline">Cancel</Button>
          </DialogClose>
          <Button type="submit" form="company-add-form" disabled={isSaving}>{isSaving ? 'Saving...' : 'Save Company'}</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
} 