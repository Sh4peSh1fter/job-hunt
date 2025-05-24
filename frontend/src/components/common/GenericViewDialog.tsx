"use client";

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
import Link from "next/link";

interface GenericViewDialogProps {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  item: Record<string, any> | null; // The item to display. Record<string, any> for flexibility.
  itemType?: string; // e.g., "Company Details", "Job Application Info"
  title?: string;
  excludedKeys?: string[]; // Keys to exclude from display (e.g., 'id', 'created_at')
}

const DEFAULT_EXCLUDED_KEYS = ['id', 'created_at', 'updated_at'];

export default function GenericViewDialog({
  isOpen,
  onOpenChange,
  item,
  itemType = "Item Details",
  title,
  excludedKeys = DEFAULT_EXCLUDED_KEYS,
}: GenericViewDialogProps) {

  if (!item) {
    return null; // Don't render if no item is provided
  }

  const dialogTitle = title || itemType;

  const renderValue = (key: string, value: any) => {
    if (value === null || value === undefined) {
      return <span className="text-muted-foreground">N/A</span>;
    }
    if (typeof value === 'boolean') {
      return value ? "Yes" : "No";
    }
    if (typeof value === 'string' && (value.startsWith('http') || value.startsWith('www'))) {
      const url = value.startsWith('www') ? `http://${value}` : value;
      return (
        <Link href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline break-all">
          {value}
        </Link>
      );
    }
    if (value instanceof Date) {
      return value.toLocaleDateString();
    }
    if (typeof value === 'object') {
      return <pre className="text-sm whitespace-pre-wrap break-all">{JSON.stringify(value, null, 2)}</pre>;
    }
    return String(value);
  };

  const filteredItemEntries = Object.entries(item).filter(
    ([key]) => !excludedKeys.includes(key)
  );

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-lg max-h-[90vh] flex flex-col">
        <DialogHeader className="flex-shrink-0">
          <DialogTitle>{dialogTitle}</DialogTitle>
          {item.name && typeof item.name === 'string' && (
            <DialogDescription>
              Viewing details for: {item.name}
            </DialogDescription>
          )}
        </DialogHeader>
        
        <div className="grid gap-4 py-4 overflow-y-auto flex-grow pr-2">
          {filteredItemEntries.length > 0 ? (
            filteredItemEntries.map(([key, value]) => (
              <div key={key} className="grid grid-cols-3 items-start gap-x-4 gap-y-1">
                <span className="font-semibold capitalize col-span-1 text-right pr-2 break-words">
                  {key.replace(/_/g, ' ')}:
                </span>
                <div className="col-span-2 break-words">
                  {renderValue(key, value)}
                </div>
              </div>
            ))
          ) : (
            <p className="text-muted-foreground">No details available for this item.</p>
          )}
        </div>

        <DialogFooter className="flex-shrink-0 pt-4">
          <DialogClose asChild>
            <Button type="button" variant="outline">Close</Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
} 