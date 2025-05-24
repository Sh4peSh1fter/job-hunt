"use client";

import { useState, useEffect, ChangeEvent, FormEvent } from 'react';
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
import { Textarea } from "@/components/ui/textarea"; // For notes or longer text fields

export interface FormFieldConfig {
  name: string;
  label: string;
  type: 'text' | 'number' | 'date' | 'url' | 'email' | 'textarea' | 'select'; // Added textarea and select
  required?: boolean;
  placeholder?: string;
  defaultValue?: string | number | null;
  options?: { value: string; label: string }[]; // For select type
  disabled?: boolean;
}

interface GenericAddDialogProps<TCreateDto extends Record<string, any>> {
  isOpen: boolean;
  onOpenChange: (isOpen: boolean) => void;
  onSave: (data: TCreateDto) => Promise<void>; // Function to handle saving the data
  formFields: FormFieldConfig[];
  itemType: string; // e.g., "Company", "Job Application"
  title?: string;
  description?: string;
  initialState?: Partial<TCreateDto>;
}

export function GenericAddDialog<TCreateDto extends Record<string, any>>({
  isOpen,
  onOpenChange,
  onSave,
  formFields,
  itemType,
  title,
  description,
  initialState = {} as TCreateDto,
}: GenericAddDialogProps<TCreateDto>) {
  const [formData, setFormData] = useState<TCreateDto>(
    initialState as TCreateDto
  );
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    // Initialize form data with default values when dialog opens or formFields change
    const initialData = { ...initialState } as TCreateDto;
    formFields.forEach((field) => {
      if (
        initialData[field.name as keyof TCreateDto] === undefined &&
        field.defaultValue !== undefined
      ) {
        initialData[field.name as keyof TCreateDto] =
          field.defaultValue as TCreateDto[keyof TCreateDto];
      } else if (initialData[field.name as keyof TCreateDto] === undefined) {
        // Ensure all fields have a default empty string or null if no explicit default
        initialData[field.name as keyof TCreateDto] = (
          field.type === "number" ? null : ""
        ) as TCreateDto[keyof TCreateDto];
      }
    });
    setFormData(initialData);
    setError(null); // Reset error when dialog opens or fields change
  }, [isOpen, formFields, initialState]);

  const handleChange = (
    e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>
  ) => {
    const { name, value, type } = e.target;

    let processedValue: string | number | null = value;

    if (type === "number") {
      processedValue = value === "" ? null : parseFloat(value);
    } else if (type === "date" && value === "") {
      processedValue = null; // Allow clearing date fields
    }


    setFormData((prev) => ({
      ...prev,
      [name]: processedValue,
    }));
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    // Convert empty string URL fields to null
    const dataToSave = { ...formData };
    formFields.forEach(field => {
      if (field.type === 'url' && dataToSave[field.name as keyof TCreateDto] === '') {
        dataToSave[field.name as keyof TCreateDto] = null as TCreateDto[keyof TCreateDto];
      }
    });


    try {
      await onSave(dataToSave);
      onOpenChange(false); // Close dialog on successful save
    } catch (err: any) {
      console.error(`Error adding ${itemType}:`, err);
      setError(
        err.message || `An unexpected error occurred while adding the ${itemType}.`
      );
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[525px] p-0">
        <DialogHeader className="p-6 pb-0">
          <DialogTitle>{title || `Add New ${itemType}`}</DialogTitle>
          {description && (
            <DialogDescription>{description}</DialogDescription>
          )}
        </DialogHeader>
        {/* Form content with scrolling */}
        <div className="flex-grow overflow-y-auto px-6">
          {error && (
            <p className="text-red-500 text-sm mb-4 bg-red-100 border border-red-400 rounded p-3">
              {error}
            </p>
          )}
          <form onSubmit={handleSubmit} id={`add-${itemType}-form`} className="space-y-4">
            {formFields.map((field) => (
              <div key={field.name} className="grid w-full items-center gap-1.5">
                <Label htmlFor={field.name}>{field.label}{field.required && "*"}</Label>
                {field.type === "textarea" ? (
                  <textarea
                    id={field.name}
                    name={field.name}
                    value={
                      formData[field.name as keyof TCreateDto] === null ||
                      formData[field.name as keyof TCreateDto] === undefined
                        ? ""
                        : String(formData[field.name as keyof TCreateDto])
                    }
                    onChange={handleChange}
                    placeholder={field.placeholder}
                    required={field.required}
                    disabled={field.disabled || isLoading}
                    rows={3}
                    className="file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex min-h-[60px] w-full rounded-md border bg-transparent px-3 py-2 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive"
                  />
                ) : field.type === "select" ? (
                  <select
                    id={field.name}
                    name={field.name}
                    value={
                      formData[field.name as keyof TCreateDto] === null ||
                      formData[field.name as keyof TCreateDto] === undefined
                        ? ""
                        : String(formData[field.name as keyof TCreateDto])
                    }
                    onChange={handleChange}
                    required={field.required}
                    disabled={field.disabled || isLoading}
                    className="file:text-foreground placeholder:text-muted-foreground selection:bg-primary selection:text-primary-foreground dark:bg-input/30 border-input flex h-9 w-full min-w-0 rounded-md border bg-transparent px-3 py-1 text-base shadow-xs transition-[color,box-shadow] outline-none file:inline-flex file:h-7 file:border-0 file:bg-transparent file:text-sm file:font-medium disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-50 md:text-sm focus-visible:border-ring focus-visible:ring-ring/50 focus-visible:ring-[3px] aria-invalid:ring-destructive/20 dark:aria-invalid:ring-destructive/40 aria-invalid:border-destructive"
                  >
                    <option value="" disabled={field.required}>
                      {field.placeholder || "Select..."}
                    </option>
                    {field.options?.map((option) => (
                      <option key={option.value} value={option.value}>
                        {option.label}
                      </option>
                    ))}
                  </select>
                ) : (
                  <Input
                    id={field.name}
                    name={field.name}
                    type={field.type}
                    value={
                      formData[field.name as keyof TCreateDto] === null ||
                      formData[field.name as keyof TCreateDto] === undefined
                        ? ""
                        : String(formData[field.name as keyof TCreateDto])
                    }
                    onChange={handleChange}
                    placeholder={field.placeholder}
                    required={field.required}
                    disabled={field.disabled || isLoading}
                  />
                )}
              </div>
            ))}
          </form>
        </div>
        <DialogFooter className="p-6 pt-4">
          <DialogClose asChild>
            <Button variant="outline" type="button" disabled={isLoading}>Cancel</Button>
          </DialogClose>
          <Button type="submit" form={`add-${itemType}-form`} disabled={isLoading}>
            {isLoading ? "Saving..." : "Save"}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
} 