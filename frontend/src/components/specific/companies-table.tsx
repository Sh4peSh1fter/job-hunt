"use client";

import { useEffect, useState } from 'react';
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
import Link from 'next/link';
import CompanyViewDialog from "./company-view-dialog";
import CompanyDeleteDialog from "./company-delete-dialog";
import { Company, CompanyUpdate } from '../../lib/types';
import { fetchCompanies, updateCompany, deleteCompany } from '../../lib/api/company-api';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter, DialogClose } from "@/components/ui/dialog";
import { Eye, Edit3, Trash2, Save, XCircle } from 'lucide-react';

export default function CompaniesTable() {
  const [companies, setCompanies] = useState<Company[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedCompanyForView, setSelectedCompanyForView] = useState<Company | null>(null);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);

  const [editingCompanyId, setEditingCompanyId] = useState<number | null>(null);
  const [editedCompanyData, setEditedCompanyData] = useState<Partial<Company> | null>(null);

  const [companyToDelete, setCompanyToDelete] = useState<Company | null>(null);
  const [isDeleteDialogOpen, setIsDeleteDialogOpen] = useState(false);

  useEffect(() => {
    async function loadCompanies() {
      try {
        setLoading(true);
        const data = await fetchCompanies();
        setCompanies(data);
        setError(null);
      } catch (err: any) {
        setError(err.message || 'Failed to load companies.');
        console.error(err);
        setCompanies([]);
      }
      setLoading(false);
    }
    loadCompanies();
  }, []);

  const handleViewCompany = (company: Company) => {
    setSelectedCompanyForView(company);
    setIsViewDialogOpen(true);
  };

  const handleEditCompany = (company: Company) => {
    setEditingCompanyId(company.id);
    setEditedCompanyData({ ...company });
  };

  const handleCancelEdit = () => {
    setEditingCompanyId(null);
    setEditedCompanyData(null);
  };

  const handleSaveEdit = async () => {
    if (!editingCompanyId || !editedCompanyData) return;
    setLoading(true);
    setError(null);
    try {
      const payload = { ...editedCompanyData } as CompanyUpdate;
      const updatedCompany = await updateCompany(editingCompanyId, payload);
      setCompanies(prevCompanies => 
        prevCompanies.map(c => c.id === editingCompanyId ? updatedCompany : c)
      );
      setEditingCompanyId(null);
      setEditedCompanyData(null);
    } catch (err: any) {
      setError(err.message || "Failed to save company changes.");
      console.error("Error saving company:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    if (!editedCompanyData) return;
    const { name, value } = event.target;
    setEditedCompanyData(prevData => ({
      ...prevData,
      [name]: value === '' ? null : value,
    }));
  };

  const openDeleteDialog = (company: Company) => {
    setCompanyToDelete(company);
    setIsDeleteDialogOpen(true);
  };

  const closeDeleteDialog = () => {
    setCompanyToDelete(null);
    setIsDeleteDialogOpen(false);
  };

  const handleDeleteConfirm = async () => {
    if (!companyToDelete) return;
    setLoading(true);
    setError(null);
    try {
      await deleteCompany(companyToDelete.id);
      setCompanies(prevCompanies => prevCompanies.filter(c => c.id !== companyToDelete.id));
      closeDeleteDialog();
    } catch (err: any) {
      setError(err.message || "Failed to delete company.");
      console.error("Error deleting company:", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p className="text-muted-foreground">Loading companies...</p>;
  }

  if (error) {
    return <p className="text-red-500">{error}</p>;
  }

  if (companies.length === 0) {
    return <p className="text-muted-foreground">No companies found.</p>;
  }

  const renderCellContent = (content: string | null | undefined, fieldName?: keyof Company, companyId?: number) => {
    if (editingCompanyId === companyId && fieldName && fieldName !== 'id' && fieldName !== 'created_at' && fieldName !== 'updated_at') {
      return (
        <Input
          type={fieldName === 'foundation_date' ? 'date' : 'text'}
          name={fieldName}
          value={editedCompanyData?.[fieldName] || ''}
          onChange={handleInputChange}
          className="h-8"
        />
      );
    }
    if (content && (String(content).startsWith('http') || String(content).startsWith('www'))) {
      const url = String(content).startsWith('www') ? `http://${String(content)}` : String(content);
      return (
        <Link href={url} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
          {content}
        </Link>
      );
    }
    return content || 'N/A';
  };

  return (
    <>
      <div className="overflow-x-auto">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Actions</TableHead>
              <TableHead>ID</TableHead>
              <TableHead>Name</TableHead>
              <TableHead>Industry</TableHead>
              <TableHead>Website</TableHead>
              <TableHead className="min-w-[200px]">Short Description</TableHead>
              <TableHead>Foundation Date</TableHead>
              <TableHead>Size</TableHead>
              <TableHead>Phase</TableHead>
              <TableHead>LinkedIn</TableHead>
              <TableHead>Crunchbase</TableHead>
              <TableHead>Glassdoor</TableHead>
              <TableHead className="min-w-[200px]">Notes</TableHead>
              <TableHead className="min-w-[200px]">Related Articles</TableHead>
              <TableHead>Created At</TableHead>
              <TableHead>Updated At</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {companies.map((company) => (
              <TableRow key={company.id}>
                <TableCell>
                  {editingCompanyId === company.id ? (
                    <>
                      <Button variant="outline" size="sm" className="mr-2 mb-1 lg:mb-0" onClick={handleSaveEdit}>Save</Button>
                      <Button variant="ghost" size="sm" onClick={handleCancelEdit}>Cancel</Button>
                    </>
                  ) : (
                    <>
                      <Button 
                        variant="outline" 
                        size="sm" 
                        className="mr-2 mb-1 lg:mb-0"
                        onClick={() => handleViewCompany(company)}
                      >
                        View
                      </Button>
                      <Button variant="outline" size="sm" className="mr-2 mb-1 lg:mb-0" onClick={() => handleEditCompany(company)}>Edit</Button>
                      <Button variant="destructive" size="sm" onClick={() => openDeleteDialog(company)}>Delete</Button>
                    </>
                  )}
                </TableCell>
                <TableCell>{company.id}</TableCell>
                <TableCell className="font-medium">{renderCellContent(company.name, 'name', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.industry, 'industry', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.website, 'website', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.short_description, 'short_description', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.foundation_date, 'foundation_date', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.size, 'size', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.phase, 'phase', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.linkedin, 'linkedin', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.crunchbase, 'crunchbase', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.glassdoor, 'glassdoor', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.notes, 'notes', company.id)}</TableCell>
                <TableCell>{renderCellContent(company.related_articles, 'related_articles', company.id)}</TableCell>
                <TableCell>{company.created_at ? new Date(company.created_at).toLocaleString() : 'N/A'}</TableCell>
                <TableCell>{company.updated_at ? new Date(company.updated_at).toLocaleString() : 'N/A'}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>
      <CompanyViewDialog 
        company={selectedCompanyForView}
        isOpen={isViewDialogOpen}
        onOpenChange={setIsViewDialogOpen}
      />
      <CompanyDeleteDialog
        company={companyToDelete}
        isOpen={isDeleteDialogOpen}
        onOpenChange={setIsDeleteDialogOpen}
        onConfirmDelete={handleDeleteConfirm}
      />
    </>
  );
} 