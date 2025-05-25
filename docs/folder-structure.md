# Folder Structure: job-hunt

**Author(s):** AI & User
**Date Proposed:** 17.5.2025 
**Status:** Adopted

---

## 1. Purpose / Scope

This document outlines the initial folder structure for the "job-hunt" project. It aims to establish a clear, maintainable, and scalable directory layout for the entire application, encompassing backend, frontend, documentation, and configuration.

---

## 2. Guiding Principles / Rationale

*   **Separation of Concerns:** Clearly separate backend (Python/FastAPI) and frontend (Next.js/React) code.
*   **Modularity:** Structure backend tools in a way that allows for easy addition and isolation of new functionalities.
*   **Clarity & Navigability:** Make it easy for developers to find code and understand the project layout.
*   **Standard Conventions:** Follow common conventions for FastAPI and Next.js projects where applicable.

---

## 3. Proposed Folder Structure

```plaintext
job-hunt/
├── backend/                  # FastAPI application and tools logic
│   ├── app/                  # Core application logic, routers, models, services
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI app instantiation and global middleware
│   │   ├── routers/          # API routers (endpoints)
│   │   │   ├── __init__.py     # Aggregates entity routers
│   │   │   ├── companies.py    # Router for Company CRUD operations
│   │   │   ├── job_applications.py # Router for JobApplication CRUD operations
│   │   │   └── job_sources.py  # Router for JobSource CRUD operations
│   │   ├── schemas/          # Pydantic schemas (formerly models/)
│   │   │   ├── __init__.py
│   │   │   ├── company.py
│   │   │   ├── job_application.py
│   │   │   └── job_source.py
│   │   │   └── application_event.py # (If ApplicationEvent is exposed via API)
│   │   ├── services/         # Business logic (currently minimal, logic mostly in routers)
│   │   │   └── __init__.py
│   │   └── db/               # Database related files
│   │       ├── __init__.py
│   │       └── database.py     # SQLAlchemy engine, session, Base
│   ├── alembic/              # Alembic migration scripts
│   ├── tests/                # Backend tests
│   └── pyproject.toml        # Poetry for dependency management
│
├── frontend/                 # Next.js frontend application
│   ├── app/                  # Next.js 13+ App Router structure
│   │   ├── (pages)/          # Main page routes (grouping without affecting URL)
│   │   │   ├── dashboard/
│   │   │   │   └── page.tsx
│   │   │   ├── components/
│   │   │   │   ├── page.tsx      # Hub page for data components
│   │   │   │   ├── companies/page.tsx
│   │   │   │   ├── job-applications/page.tsx
│   │   │   │   └── job-sources/page.tsx
│   │   │   ├── guide/page.tsx
│   │   │   └── tools/page.tsx
│   │   ├── layout.tsx        # Root layout
│   │   └── globals.css
│   ├── components/           # Reusable React components
│   │   ├── ui/               # Shadcn/UI components (vendored)
│   │   ├── common/           # Generic, reusable application components (GenericDataTable, etc.)
│   │   └── specific/         # Components specific to features/tools (currently less used due to generic components)
│   ├── lib/                  # Utility functions, constants, type definitions
│   │   ├── types.ts          # Core frontend type definitions
│   │   ├── api/              # API interaction utility functions (company-api.ts, etc.)
│   │   └── utils.ts          # General utility functions
│   ├── public/               # Static assets
│   ├── styles/               # Additional global styles (if needed)
│   ├── tests/                # Frontend tests
│   └── package.json          # Frontend dependencies and scripts
│
├── docs/                     # Project documentation
│   ├── PRD.md                # Product Requirements Document
│   ├── tech-stack.md         # Technology Stack
│   ├── folder-structure.md   # This document
│   ├── adr/                  # Architecture Decision Records
│   │   └── ADR-001-database-choice.md
│   ├── rules/                # Cursor AI rules
│   ├── templates/            # Document templates
│   └── README.md             # Overview of the /docs directory
│
├── .cursor/                  # Cursor-specific configuration and rules (as .mdc files)
├── .gitignore                # Specifies intentionally untracked files that Git should ignore
└── README.md                 # Project-level README (overview, setup, run)
```

---

## 4. Key Directory Explanations

*   **`backend/app/routers/`**: Contains FastAPI routers for each data entity. `__init__.py` includes these into a main API router with specific prefixes (e.g., `/api/v1/companies`, `/api/v1/job-apps`).
*   **`backend/app/schemas/`**: Houses Pydantic schemas used for request/response validation and data representation, replacing the older `models/` directory for this purpose. SQLAlchemy models (if used more directly for DB schema definition beyond Alembic) might reside in `db/` or a dedicated `orm_models/` directory.
*   **`frontend/components/ui/`**: Stores components added via Shadcn/UI CLI. These are considered part of the project's codebase and can be customized.
*   **`frontend/components/common/`**: Home for generic, reusable UI components like `GenericDataTable.tsx`, `GenericAddDialog.tsx`, etc., which form the core of the dynamic data pages.
*   **`frontend/lib/api/`**: Contains typed functions for making API calls to the backend, abstracting fetch logic for each entity.

---

## 5. Naming Conventions

*   **Folders:** `kebab-case` for multi-word folder names (e.g., `company-research`). `snake_case` for Python package directories if preferred (though kebab-case is also fine for top-level tool directories if they aren't Python packages themselves).
*   **Files:**
    *   **Python:** `snake_case.py` (e.g., `tools_router.py`, `processor.py`).
    *   **Next.js/React Components:** `PascalCase.tsx` (e.g., `ToolCard.tsx`).
    *   **Next.js Pages/Layouts:** `page.tsx`, `layout.tsx` (as per Next.js App Router conventions).
    *   **Markdown:** `kebab-case.md` (e.g., `folder-structure.md`).

---

## 6. Impact on Existing Structure

This is the initial proposed structure for a new project.

---

## 7. Open Questions / Areas for Discussion

*   Confirm preference for Python dependency management (`requirements.txt` vs. `pyproject.toml` with Poetry/PDM).
*   Decision on whether to use a UI component library like Shadcn/UI or build all components from scratch with Tailwind CSS in `frontend/components/ui/`.

---

## 8. Next Steps

*   Review and approve this folder structure.
*   Initialize project directories and boilerplate code according to this structure.
