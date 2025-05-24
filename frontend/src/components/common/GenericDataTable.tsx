"use client";

import React, { useState, useEffect, ChangeEvent } from 'react';
import {
  Table,
  TableHeader,
  TableBody,
  TableRow,
  TableHead,
  TableCell,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Eye, Edit3, Trash2, Save, XCircle } from 'lucide-react';
import Link from 'next/link';
import { FormFieldConfig } from './GenericAddDialog';

// Generic type for any data item that has an ID
export interface DataItem {
  id: number;
  [key: string]: any; // Allow other properties
}

export interface ColumnConfig<T extends DataItem> {
  accessorKey: keyof T | 'actions';
  header: string;
  cellContent?: (item: T) => React.ReactNode;
  enableEdit?: boolean;
  inputType?: 'text' | 'number' | 'date' | 'url' | 'email' | 'textarea' | 'select';
  options?: { value: string; label: string }[];
  minWidth?: string;
  formFieldConfig?: FormFieldConfig;
}

interface GenericDataTableProps<T extends DataItem> {
  columns: ColumnConfig<T>[];
  data: T[];
  isLoading: boolean;
  error: string | null;
  onView?: (item: T) => void;
  onEdit?: (item: T) => void;
  onSaveEdit: (originalItem: T, editedData: Partial<T>) => Promise<void>;
  onDelete?: (item: T) => void;
  itemType?: string;
}

export default function GenericDataTable<T extends DataItem>({
  columns,
  data,
  isLoading,
  error,
  onView,
  onEdit,
  onSaveEdit,
  onDelete,
  itemType = "items",
}: GenericDataTableProps<T>) {
  const [editingItemId, setEditingItemId] = useState<number | null>(null);
  const [editedItemData, setEditedItemData] = useState<Partial<T> | null>(null);
  const [isSaving, setIsSaving] = useState(false);
  const [internalError, setInternalError] = useState<string | null>(null);

  useEffect(() => {
    // Reset editing state if data changes (e.g., after delete/add elsewhere)
    setEditingItemId(null);
    setEditedItemData(null);
  }, [data]);

  const startEdit = (item: T) => {
    setEditingItemId(item.id);
    setEditedItemData({ ...item });
    setInternalError(null);
    if (onEdit) onEdit(item); // Call parent's onEdit if provided
  };

  const cancelEdit = () => {
    setEditingItemId(null);
    setEditedItemData(null);
    setInternalError(null);
  };

  const saveEdit = async () => {
    if (!editingItemId || !editedItemData) return;
    setIsSaving(true);
    setInternalError(null);
    try {
      const originalItem = data.find(item => item.id === editingItemId);
      if (!originalItem) throw new Error("Original item not found for saving.");
      await onSaveEdit(originalItem, editedItemData);
      setEditingItemId(null);
      setEditedItemData(null);
    } catch (err: any) {
      console.error(`Error saving ${itemType}:`, err);
      setInternalError(err.message || `Failed to save ${itemType}.`);
      // Do not cancel edit on error, allow user to retry or cancel
    } finally {
      setIsSaving(false);
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value, type } = e.target;
    let processedValue: string | number | boolean | null = value;
    //Find the column config for the current field
    const columnConfig = columns.find(col => col.accessorKey === name);

    if (columnConfig?.inputType === 'number') {
      processedValue = value === '' ? null : parseFloat(value);
    } else if (type === 'checkbox') {
      processedValue = (e.target as HTMLInputElement).checked;
    } else if (columnConfig?.inputType === 'date' && value === '') {
      processedValue = null;
    }
    
    setEditedItemData((prev) => ({
      ...prev,
      [name]: processedValue,
    } as Partial<T>));
  };

  const handleSelectChange = (name: string, value: string) => {
    setEditedItemData((prev) => ({
        ...prev,
        [name]: value,
    } as Partial<T>));
  };

  const renderCellContent = (item: T, column: ColumnConfig<T>) => {
    const content = item[column.accessorKey as keyof T];

    if (column.cellContent) {
        return column.cellContent(item);
    }

    if (editingItemId === item.id && column.enableEdit && column.accessorKey !== 'actions') {
        const fieldName = column.accessorKey as string;
        const currentValue = editedItemData?.[fieldName] ?? '';
        const inputType = column.inputType || 'text';

        if (inputType === 'select' && column.options) {
            return (
                <Select 
                    name={fieldName} 
                    value={String(currentValue)} 
                    onValueChange={(value) => handleSelectChange(fieldName, value)}
                    disabled={isSaving}
                >
                    <SelectTrigger className="h-8 w-full">
                        <SelectValue placeholder={column.header || "Select..."} />
                    </SelectTrigger>
                    <SelectContent>
                        {column.options.map(option => (
                            <SelectItem key={option.value} value={option.value}>
                                {option.label}
                            </SelectItem>
                        ))}
                    </SelectContent>
                </Select>
            );
        }
        if (inputType === 'textarea') {
            return (
                <Textarea
                    name={fieldName}
                    value={String(currentValue)}
                    onChange={handleInputChange}
                    disabled={isSaving}
                    className="h-auto text-xs"
                    rows={2}
                />
            );
        }
        return (
            <Input
                type={inputType}
                name={fieldName}
                value={String(currentValue)}
                onChange={handleInputChange}
                disabled={isSaving}
                className="h-8 text-xs"
            />
        );
    }

    if (typeof content === 'boolean') {
      return content ? 'Yes' : 'No';
    }
    // Cast content to any for instanceof check if linter is strict
    if (typeof content === 'object' && content !== null && (content as any) instanceof Date) {
      return content.toLocaleDateString();
    }
    if (column.inputType === 'url' && typeof content === 'string' && content) {
        const url = content.startsWith('http') ? content : `http://${content}`;
        return <Link href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">Link</Link>;
    }
    return content ? String(content) : 'N/A';
  };

  if (isLoading) {
    return <p className="text-center text-muted-foreground py-4">Loading {itemType}...</p>;
  }

  if (error && !data.length) {
    return <p className="text-center text-red-500 py-4">Error: {error}</p>;
  }

  if (!data.length) {
    return <p className="text-center text-muted-foreground py-4">No {itemType} found.</p>;
  }

  return (
    <>
      {internalError && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
          <strong className="font-bold">Error: </strong>
          <span className="block sm:inline">{internalError}</span>
        </div>
      )}
      <div className="overflow-x-auto rounded-md border">
        <Table>
          <TableHeader>
            <TableRow>
              {columns.map((column) => (
                <TableHead key={String(column.accessorKey)} style={{minWidth: column.minWidth}}>
                  {column.header}
                </TableHead>
              ))}
            </TableRow>
          </TableHeader>
          <TableBody>
            {data.map((item) => (
              <TableRow key={item.id}>
                {columns.map((column) => (
                  <TableCell key={`${item.id}-${String(column.accessorKey)}`}>
                    {column.accessorKey === 'actions' ? (
                      <div className="flex space-x-2">
                        {editingItemId === item.id ? (
                          <>
                            <Button variant="outline" size="sm" onClick={saveEdit} disabled={isSaving} className="text-xs px-2 py-1 h-auto">
                              <Save className="mr-1 h-3 w-3" /> {isSaving ? 'Saving...' : 'Save'}
                            </Button>
                            <Button variant="ghost" size="sm" onClick={cancelEdit} disabled={isSaving} className="text-xs px-2 py-1 h-auto">
                              <XCircle className="mr-1 h-3 w-3" /> Cancel
                            </Button>
                          </>
                        ) : (
                          <>
                            {onView && (
                              <Button variant="outline" size="sm" onClick={() => onView(item)} className="text-xs px-2 py-1 h-auto">
                                <Eye className="mr-1 h-3 w-3" /> View
                              </Button>
                            )}
                            {(column.enableEdit === undefined || column.enableEdit === true) && typeof onSaveEdit === 'function' && (
                                <Button variant="outline" size="sm" onClick={() => startEdit(item)} className="text-xs px-2 py-1 h-auto">
                                    <Edit3 className="mr-1 h-3 w-3" /> Edit
                                </Button>
                            )}
                            {onDelete && (
                              <Button variant="destructive" size="sm" onClick={() => onDelete(item)} className="text-xs px-2 py-1 h-auto">
                                <Trash2 className="mr-1 h-3 w-3" /> Delete
                              </Button>
                            )}
                          </>
                        )}
                      </div>
                    ) : (
                      renderCellContent(item, column)
                    )}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
    </>
  );
} 