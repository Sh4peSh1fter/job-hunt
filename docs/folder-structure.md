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
│   │   │   ├── __init__.py
│   │   │   └── tools_router.py # Example router for tools
│   │   ├── models/           # Pydantic models for request/response, data models
│   │   │   └── __init__.py
│   │   ├── services/         # Business logic, services interacting with tools/DB
│   │   │   └── __init__.py
│   │   └── db/               # Database related files (e.g., schema, connection, migrations if needed)
│   │       ├── __init__.py
│   │       └── database.py     # SQLite connection setup, ORM setup (e.g. SQLAlchemy)
│   ├── tools/                  # Individual tool modules
│   │   ├── __init__.py
│   │   ├── keyword_analyzer/ # Example tool: Keyword Frequency Analyzer
│   │   │   ├── __init__.py
│   │   │   └── processor.py  # Logic for this specific tool
│   │   └── company_research/ # Example tool: Company Research Assistant
│   │       ├── __init__.py
│   │       └── assistant.py  # Logic for this specific tool
│   ├── tests/                # Backend tests
│   │   └── __init__.py
│   └── requirements.txt      # Python dependencies (or pyproject.toml if using Poetry)
│
├── frontend/                 # Next.js frontend application
│   ├── app/                  # Next.js 13+ App Router structure
│   │   ├── (pages)/          # Main page routes
│   │   │   ├── layout.tsx    # Root layout
│   │   │   ├── page.tsx      # Homepage
│   │   │   ├── guide/        # Guide page (job searching philosophy)
│   │   │   │   └── page.tsx
│   │   │   └── tools/        # Tools listing/launcher page
│   │   │       ├── page.tsx
│   │   │       └── [toolSlug]/ # Dynamic route for individual tools
│   │   │           └── page.tsx
│   │   └── globals.css
│   ├── components/           # Reusable React components
│   │   ├── ui/               # Generic UI elements (buttons, cards, etc. - from Shadcn/ui or similar if used)
│   │   └── specific/         # Components specific to features/tools
│   ├── lib/                  # Utility functions, constants, etc.
│   ├── public/               # Static assets (images, fonts, etc.)
│   ├── styles/               # Global styles (if not solely using Tailwind in components)
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

*   **`backend/`**: Contains all Python code for the FastAPI server.
    *   **`backend/app/`**: Core application components like routers, Pydantic models, service logic, and database interaction.
    *   **`backend/tools/`**: Each subdirectory here represents a distinct tool. This promotes modularity, allowing tools to be developed and maintained somewhat independently. Each tool will contain its own processing logic.
    *   **`backend/tests/`**: Unit and integration tests for the backend.
*   **`frontend/`**: Contains all Next.js/React code for the user interface.
    *   **`frontend/app/`**: Utilizes the Next.js App Router for routing and layouts.
        *   `frontend/app/(pages)/`: Main page routes like homepage, guide, and tools.
        *   `frontend/app/(pages)/tools/[toolSlug]/`: Dynamic routes for individual tool interfaces.
    *   **`frontend/components/`**: Reusable React components, potentially split into generic UI elements and feature-specific components.
    *   **`frontend/lib/`**: Client-side utility functions.
    *   **`frontend/tests/`**: Unit and integration tests for frontend components.
*   **`docs/`**: All project-related documentation, including PRD, ADRs, tech stack, rules, and this folder structure document.
*   **`.cursor/`**: Contains the `.mdc` rule files for AI guidance.

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
