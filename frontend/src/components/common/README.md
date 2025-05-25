# Common Frontend Components

This directory (`frontend/src/components/common/`) houses generic, reusable React components that form the building blocks for various parts of the Job Hunt application, particularly the data management pages (Companies, Job Applications, Job Sources).

These components are designed to be configurable and adaptable to different data types and backend entities.

## Core Generic Components

### 1. `GenericDataTable.tsx`

-   **Purpose:** Provides a highly configurable table for displaying, editing, viewing, and deleting data items fetched from the backend API.
-   **Key Features:**
    -   Dynamic column rendering based on a `ColumnConfig` prop.
    -   Inline editing capabilities for specified fields (text, number, select, date, textarea).
    -   Integration with `GenericViewDialog` for detailed item viewing.
    -   Integration with `GenericDeleteDialog` for item deletion with confirmation.
    -   Client-side pagination (can be extended for server-side).
    -   Loading and error states.
-   **Core Props:**
    -   `columns`: `ColumnConfig<T>[]` - Defines table columns, their accessors, headers, and editability.
    -   `data`: `T[]` - The array of data items to display.
    -   `itemType`: `string` - A string descriptor for the item type (e.g., "Company"), used in dialog titles and messages.
    -   `onView`: `(item: T) => void` - Handler for the "View" action.
    -   `onEdit`: `(item: T) => void` - Handler for initiating the "Edit" action (typically opens an add/edit dialog).
    -   `onSaveEdit`: `(updatedItem: Partial<T>, originalItem: T) => Promise<void>` - Handler for saving inline edits.
    -   `onDelete`: `(item: T) => void` - Handler for the "Delete" action.
    -   `isLoading`: `boolean` - Indicates if data is currently loading.
    -   `error`: `string | null` - Displays an error message if present.

### 2. `GenericAddDialog.tsx`

-   **Purpose:** A dialog component for creating new items or editing existing ones (when used for full-form edit).
-   **Key Features:**
    -   Dynamically generates form fields based on a `FormFieldConfig` prop.
    -   Supports various input types (text, number, textarea, select, date).
    -   Handles form state, validation (basic, can be extended), and submission.
    -   Manages loading and error states during save operations.
-   **Core Props:**
    -   `isOpen`, `onOpenChange`: Standard dialog control props.
    -   `onSave`: `(formData: TCreateDto) => Promise<void>` - Handler for saving the form data.
    -   `formFields`: `FormFieldConfig<TCreateDto>[]` - Defines the form fields, their names, labels, types, and options (for select).
    -   `itemType`: `string` - Descriptor for the item type.
    -   `title`, `description`: Optional dialog title and description.
    -   `initialState`: `Partial<TCreateDto>` - Pre-populates the form for editing.

### 3. `GenericViewDialog.tsx`

-   **Purpose:** A simple dialog to display the details of an item in a read-only format.
-   **Key Features:**
    -   Renders item details based on provided `itemData` and `viewFields` configuration.
    -   Handles different data types for display (strings, numbers, dates, booleans, links).
-   **Core Props:**
    -   `isOpen`, `onOpenChange`: Dialog control.
    -   `itemData`: `T | null` - The data item to display.
    -   `viewFields`: `{ key: keyof T; label: string; type?: 'string' | 'date' | 'url' | 'boolean' }[]` - Configuration for which fields to display and how.
    -   `itemType`: `string` - Descriptor for the item type.

### 4. `GenericDeleteDialog.tsx`

-   **Purpose:** Provides a confirmation dialog before deleting an item.
-   **Key Features:**
    -   Standard alert dialog pattern for destructive actions.
    -   Manages loading state during the delete operation.
-   **Core Props:**
    -   `isOpen`, `onOpenChange`: Dialog control.
    -   `onConfirmDelete`: `() => Promise<void>` - Handler for confirming the deletion.
    -   `itemName`: `string` - Name of the item being deleted, used in the confirmation message.
    -   `itemType`: `string` - Descriptor for the item type.
    -   `isLoading`: `boolean` - Indicates if deletion is in progress.

## Usage Pattern

Typically, a page component (e.g., `companies/page.tsx`) will:
1.  Fetch data for the entity.
2.  Define `ColumnConfig` and `FormFieldConfig` specific to that entity.
3.  Manage state for dialog visibility and currently selected/editing items.
4.  Pass data and configuration to these generic components.
5.  Implement handler functions (`handleAdd`, `handleUpdate`, `handleDelete`, etc.) that interact with the backend API (via `frontend/src/lib/api/`) and update the local data state.

This approach promotes code reuse and consistency across different data management sections of the application. 