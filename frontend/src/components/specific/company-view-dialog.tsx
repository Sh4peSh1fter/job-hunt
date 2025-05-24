"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface Company {
  id: number;
  name: string;
  foundation_date: string | null;
  industry: string | null;
  size: string | null;
  phase: string | null;
  website: string | null;
  linkedin: string | null;
  crunchbase: string | null;
  glassdoor: string | null;
  short_description: string | null;
  notes: string | null;
  related_articles: string | null;
  created_at: string;
  updated_at: string;
}

interface CompanyViewDialogProps {
  company: Company | null;
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
}

export default function CompanyViewDialog({ company, isOpen, onOpenChange }: CompanyViewDialogProps) {
  if (!company) {
    return null;
  }

  const renderDetail = (label: string, value: string | number | null | undefined) => {
    let displayValue: React.ReactNode = value || 'N/A';
    if (typeof value === 'string' && (value.startsWith('http') || value.startsWith('www'))) {
      const url = value.startsWith('www') ? `http://${value}` : value;
      displayValue = (
        <a href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
          {value}
        </a>
      );
    } else if (label.includes('Date') && value) {
        try {
            displayValue = new Date(value as string).toLocaleDateString();
        } catch (e) {
            // If parsing fails, display original value
            displayValue = value;
        }
    } else if (label.includes('At') && value) { // For Created At / Updated At
        try {
            displayValue = new Date(value as string).toLocaleString();
        } catch (e) {
            displayValue = value;
        }
    }


    return (
      <div className="mb-3">
        <h4 className="text-sm font-semibold text-gray-600">{label}</h4>
        <p className="text-gray-800">{displayValue}</p>
      </div>
    );
  };

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>{company.name}</DialogTitle>
          <DialogDescription>
            Detailed information for {company.name}.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          {/* {renderDetail("ID", company.id)} */}
          {renderDetail("Industry", company.industry)}
          {renderDetail("Website", company.website)}
          {renderDetail("Short Description", company.short_description)}
          {renderDetail("Foundation Date", company.foundation_date)}
          {renderDetail("Size", company.size)}
          {renderDetail("Phase", company.phase)}
          {renderDetail("LinkedIn", company.linkedin)}
          {renderDetail("Crunchbase", company.crunchbase)}
          {renderDetail("Glassdoor", company.glassdoor)}
          {renderDetail("Notes", company.notes)}
          {renderDetail("Related Articles", company.related_articles)}
          {renderDetail("Created At", company.created_at)}
          {renderDetail("Updated At", company.updated_at)}
        </div>
        <DialogFooter>
          <Button onClick={() => onOpenChange(false)}>Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
} 