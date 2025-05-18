# job-hunt: Initial Setup & Core Features Task List

**Last Updated:** 17.5.2025 

This document outlines the initial tasks to set up the "job-hunt" project structure, core application, and foundational features as defined in the PRD.

---

## 🎯 Next Up / In Progress Tasks

### Phase 1: Project Foundation & Backend Setup

- [ ] **Task Title:** Initialize Python project with Poetry and add initial dependencies. (Assignee: [Dev], PRD: `docs/PRD.md#6.1`, Due: [Date])
    - *Notes:* `pyproject.toml` with Python, FastAPI, Uvicorn, Pydantic, SQLAlchemy, aiosqlite, Ruff, Pytest, httpx, Alembic, google-api-python-client, gspread. Run `poetry lock && poetry install`.
- [ ] **Task Title:** Create Supabase project and configure environment variables. (Assignee: [Dev], PRD: `docs/PRD.md#6.3.1`, Due: [Date])
    - *Notes:* Set up a new project in Supabase. Create a `.env` file in `backend/` with `SUPABASE_URL` and `SUPABASE_KEY` (anon key for now). Add `.env` to `.gitignore`.
- [ ] **Task Title:** Implement Supabase client initialization and configuration. (Assignee: [Dev], PRD: `docs/PRD.md#6.3.1`, Due: [Date])
    - *Notes:* Create `backend/app/config.py` (Pydantic BaseSettings) and `backend/app/core/supabase_client.py` as per `docs/rules/backend.md`.
- [ ] **Task Title:** Create initial FastAPI application structure. (Assignee: [Dev], PRD: `docs/PRD.md#6.1`, Due: [Date])
    - *Notes:* Implement base according to `docs/folder-structure.md` and `docs/rules/backend.md`. Create `main.py`, `app/db/database.py` (async setup), `app/models/` folders.
- [ ] **Task Title:** Setup SQLite database and SQLAlchemy ORM. (Assignee: [Dev], PRD: `docs/PRD.md#6.3`, Due: [Date])
    - *Notes:* Define `Base`, `AsyncSessionLocal`, `async_engine` in `app/db/database.py`. Implement `get_async_db` dependency. Create basic ORM models for a generic "ToolOutput" or similar if needed for early tools in `app/models/`.
- [ ] **Task Title:** Implement Alembic for database migrations. (Assignee: [Dev], PRD: `docs/PRD.md#6.3`, Due: [Date])
    - *Notes:* Configure Alembic for async SQLAlchemy with SQLite (e.g., in `backend/alembic/` or `backend/app/db/`). Create initial migration based on models.
- [ ] **Task Title:** Setup basic API endpoint for testing database connection. (Assignee: [Dev], PRD: `docs/PRD.md#6.1`, Due: [Date])
    - *Notes:* Simple `/health` or `/ping` endpoint in FastAPI that performs a basic query using SQLAlchemy session (e.g., `session.execute(select(1))`) to verify DB connection.
- [ ] **Task Title:** Define initial SQLAlchemy models. (Assignee: [Dev], PRD: `docs/PRD.md#6.3`, Due: [Date])
    - *Notes:* Create initial models in `backend/app/models/` (e.g., for JobApplication, Company, Contact). Ensure they inherit from `Base` in `app.db.database`.

### Phase 2: Frontend Setup

- [ ] **Task Title:** Initialize Next.js project. (Assignee: [Dev], PRD: `docs/PRD.md#6.2`, Due: [Date])
    - *Notes:* Use `create-next-app`. Setup according to `docs/folder-structure.md` and `docs/rules/frontend.md` (App Router).
- [ ] **Task Title:** Integrate Tailwind CSS. (Assignee: [Dev], PRD: `docs/PRD.md#6.2`, Due: [Date])
    - *Notes:* Configure Tailwind CSS and PostCSS as per Next.js guidelines.
- [ ] **Task Title:** Setup Shadcn/UI. (Assignee: [Dev], PRD: `docs/PRD.md#6.2`, Due: [Date])
    - *Notes:* Initialize Shadcn/UI and add a few basic components (e.g., Button, Card).
- [ ] **Task Title:** Create basic frontend layout and navigation. (Assignee: [Dev], PRD: `docs/PRD.md#4.1`, `docs/PRD.md#5.1`, Due: [Date])
    - *Notes:* Based on Tailwind Next.js Starter Blog. Implement root layout, header, and placeholders for "Homepage/Guide" and "Tools" sections.
- [ ] **Task Title:** Implement static Homepage/Guide page. (Assignee: [Dev], PRD: `docs/PRD.md#5.1`, Due: [Date])
    - *Notes:* Create a simple page to display Markdown content from `docs/guide.md` (to be created).

### Phase 3: First Tool - Keyword Frequency Analyzer

- [ ] **Task Title:** Design backend API for Keyword Frequency Analyzer. (Assignee: [Dev], PRD: `docs/PRD.md#5.2.1`, Due: [Date])
    - *Notes:* Define Pydantic models for request (job description text) and response (keyword counts). Create FastAPI router and endpoint.
- [ ] **Task Title:** Implement backend logic for Keyword Frequency Analyzer. (Assignee: [Dev], PRD: `docs/PRD.md#5.2.1`, Due: [Date])
    - *Notes:* Core Python logic to process text and count word frequencies. Consider simple NLP for stop-word removal.
- [ ] **Task Title:** Create frontend UI for Keyword Frequency Analyzer. (Assignee: [Dev], PRD: `docs/PRD.md#5.2.1`, Due: [Date])
    - *Notes:* Text input area, submit button, display area for results (table/list).
- [ ] **Task Title:** Integrate Keyword Frequency Analyzer frontend with backend. (Assignee: [Dev], PRD: `docs/PRD.md#5.2.1`, Due: [Date])
    - *Notes:* Fetch call from Next.js to FastAPI.

---

## ⏳ Future Tasks / Backlog

- [ ] **Feature/Task Idea:** Company Research Assistant (Backend API & Logic). (PRD: `docs/PRD.md#5.2.2`)
- [ ] **Feature/Task Idea:** Company Research Assistant (Frontend UI & Integration). (PRD: `docs/PRD.md#5.2.2`)
- [ ] **Feature/Task Idea:** Resume Tailoring Utility (Backend API & Logic). (PRD: `docs/PRD.md#5.2.3`)
- [ ] **Feature/Task Idea:** Resume Tailoring Utility (Frontend UI & Integration). (PRD: `docs/PRD.md#5.2.3`)
- [ ] **Feature/Task Idea:** Implement SQLite data persistence for tool outputs. (PRD: `docs/PRD.md#6.3`)
- [ ] **Feature/Task Idea:** Implement CSV export functionality. (PRD: `docs/PRD.md#6.3`)
- [ ] **Feature/Task Idea:** Implement Google Sheets synchronization (Optional Feature - Backend). (PRD: `docs/PRD.md#6.3`)
- [ ] **Feature/Task Idea:** Implement Google Sheets synchronization (Optional Feature - Frontend UI & Auth). (PRD: `docs/PRD.md#6.3`)
- [ ] **Task Title:** Setup backend testing framework (Pytest). (Assignee: [Dev], PRD: `docs/tech-stack.md#5. Testing`)
- [ ] **Task Title:** Write unit/integration tests for backend. (Assignee: [Dev])
- [ ] **Task Title:** Setup frontend testing framework (Jest & React Testing Library). (Assignee: [Dev], PRD: `docs/tech-stack.md#5. Testing`)
- [ ] **Task Title:** Write component/unit tests for frontend. (Assignee: [Dev])
- [ ] **Task Title:** Setup Linters/Formatters (Ruff, ESLint, Prettier). (Assignee: [Dev], PRD: `docs/tech-stack.md#6. Linting Formatting`)
- [ ] **Task Title:** Create `docs/guide.md` with initial job search guidance content.
- [ ] **Research Topic:** Explore best NLP libraries for more advanced keyword extraction and resume analysis (e.g., spaCy, NLTK).

---

## ✅ Completed Tasks

- [x] **Completed Task Title:** Define initial PRD. (Completed: 17.5.2025, Relevant Files: `docs/PRD.md`)
- [x] **Completed Task Title:** Decide on Database and Document in ADR. (Completed: October 26, 2023, Relevant Files: `docs/adr/ADR-001-database-choice.md`)
- [x] **Completed Task Title:** Define Technology Stack. (Completed: 17.5.2025, Relevant Files: `docs/tech-stack.md`)
- [x] **Completed Task Title:** Define Folder Structure. (Completed: 17.5.2025, Relevant Files: `docs/folder-structure.md`)
- [x] **Completed Task Title:** Update Backend & Frontend Rules. (Completed: 17.5.2025, Relevant Files: `docs/rules/backend.md`, `docs/rules/frontend.md`)
- [x] **Completed Task Title:** Initialize Python project with Poetry and add initial dependencies. (Completed: October 26, 2023, Relevant Files: `backend/pyproject.toml`)
- [x] **Completed Task Title:** Create initial FastAPI application structure and health check. (Completed: October 26, 2023, Relevant Files: `backend/app/main.py`, `backend/app/config.py`, `backend/app/db/database.py`)
- [x] **Completed Task Title:** Setup SQLite database and SQLAlchemy ORM. (Completed: October 26, 2023, Relevant Files: `backend/app/db/database.py`)
- [x] **Completed Task Title:** Implement Alembic for database migrations (Initial Setup). (Completed: October 26, 2023, Relevant Files: `backend/alembic.ini`, `backend/alembic/env.py`)
- [x] **Completed Task Title:** Define initial SQLAlchemy models and Enums. (Completed: October 26, 2023, Relevant Files: `backend/app/models/`)
- [x] **Completed Task Title:** Generate and apply initial Alembic migration. (Completed: October 26, 2023, Relevant Files: `backend/alembic/versions/`)
- [x] **Completed Task Title:** Setup/Verify API endpoint for testing database connection. (Completed: October 26, 2023, Relevant Files: `backend/app/main.py`)
- [x] **Completed Task Title:** Setup backend testing framework (Pytest) with initial test. (Completed: October 26, 2023, Relevant Files: `backend/pyproject.toml`, `backend/tests/test_main.py`)
- [x] **Completed Task Title:** Setup Linters/Formatters (Ruff) and run initial checks. (Completed: October 26, 2023, Relevant Files: `backend/pyproject.toml`)

---

## 📝 Implementation Plan / Notes

### Initial Development Focus

-   **Strategy:** Prioritize setting up the foundational structures for both backend and frontend. Then, implement the first tool (Keyword Frequency Analyzer) end-to-end to establish a pattern for subsequent tools.
-   **Key Components:** FastAPI application, Next.js application, SQLite database, core tool logic modules.
-   **Open Questions/Risks:** 
    -   Complexity of Google Sheets integration and authentication flow.
    -   Ensuring the local-first approach is maintained even with optional cloud features.

---

## 📂 Relevant Files & Links

-   **Project Documentation:**
    -   `docs/PRD.md` - Main Product Requirements Document.
    -   `docs/folder-structure.md` - Project Folder Structure.
    -   `docs/tech-stack.md` - Technology Stack.
    -   `docs/rules/backend.md` - Backend Development Rules.
    -   `docs/rules/frontend.md` - Frontend Development Rules.
    -   `docs/adr/ADR-001-database-choice.md` - Database Choice ADR.
-   **Key Source Files (Examples to be created):**
    -   `backend/app/main.py`
    -   `backend/app/db/database.py`
    -   `frontend/app/layout.tsx`
    -   `frontend/app/(pages)/page.tsx` (Homepage)
    -   `frontend/app/(pages)/tools/page.tsx` (Tools landing)
-   **External Resources:**
    -   FastAPI Documentation: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
    -   Next.js Documentation: [https://nextjs.org/docs](https://nextjs.org/docs)
    -   SQLAlchemy Documentation: [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
    -   Tailwind CSS Documentation: [https://tailwindcss.com/docs](https://tailwindcss.com/docs)
    -   Shadcn/UI: [https://ui.shadcn.com/](https://ui.shadcn.com/)

---

**Instructions for using this template:**

1.  **Replace Placeholders:** Fill in all bracketed placeholders (e.g., `[Project Name]`, `[YYYY-MM-DD]`, `[Name/Team]`) with specific information.
2.  **Task Detail:** For "Next Up" tasks, provide enough detail for someone to understand and start working on them.
3.  **Maintain Sections:** Keep the defined sections updated as the project progresses.
4.  **Date Format:** Use YYYY-MM-DD for consistency.
5.  **PRD Links:** Actively link tasks back to the Product Requirements Document (`docs/PRD.md`) or specific issue trackers for traceability. 
