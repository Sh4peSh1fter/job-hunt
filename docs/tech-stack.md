# Technology Stack: job-hunt

**Author(s):** AI & User
**Date Proposed:** 17.5.2025 
**Status:** Adopted

---

## 1. Purpose / Scope

This document outlines the initial technology stack for the "job-hunt" project. It serves as the definitive record of core technologies chosen for the development of this local web application.

---

## 2. Guiding Principles for this Proposal

*   **Simplicity & Ease of Use:** Prefer technologies that are straightforward to set up and use for a local application.
*   **Performance:** Choose technologies capable of delivering a responsive user experience.
*   **Privacy-Focused:** Ensure the stack supports a fully local, self-hosted deployment.
*   **Modularity & Extensibility:** Select technologies that allow for easy expansion of features (e.g., adding new tools).
*   **Strong Community Support & Documentation:** Prefer well-documented and widely-used technologies.

---

## 3. Core Stack Overview

The "job-hunt" project will be a web application with a Python/FastAPI backend and a Next.js/React frontend. Data will be stored locally using SQLite. The application is designed to run entirely on the user's machine.

---

## 4. Documented Technologies

### Frontend Technologies

-   **Technology Name:** Next.js
    -   **Current/Proposed Version(s):** Latest stable (e.g., ^14.x.x)
    -   **Purpose/Role in Project:** Full-stack React framework for building the user interface and handling client-side logic. Will serve static documentation pages and the tools interface.
    -   **Rationale/Decision Date:** Chosen for its comprehensive feature set for React development, SSR/SSG capabilities, routing, and good integration with Tailwind CSS. (Decision: 17.5.2025)
    -   **Key Libraries/Plugins Used (if any):** React

-   **Technology Name:** React
    -   **Current/Proposed Version(s):** Latest stable (e.g., ^18.x.x - managed by Next.js)
    -   **Purpose/Role in Project:** Core UI library for building interactive components.
    -   **Rationale/Decision Date:** Industry standard for building modern web UIs, native to Next.js. (Implicit with Next.js)

-   **Technology Name:** Tailwind CSS
    -   **Current/Proposed Version(s):** Latest stable (e.g., ^3.x.x)
    -   **Purpose/Role in Project:** Utility-first CSS framework for styling the application.
    -   **Rationale/Decision Date:** Allows for rapid UI development and customization. The visual style will be based on the Tailwind Next.js Starter Blog. (Decision: 17.5.2025)

-   **Technology Name:** Markdown
    -   **Current/Proposed Version(s):** N/A
    -   **Purpose/Role in Project:** For creating and managing static content, such as the homepage guide and documentation.
    -   **Rationale/Decision Date:** Simple and effective for text-based content. (Decision: 17.5.2025)

-   **Technology Name:** Shadcn/UI
    -   **Current/Proposed Version(s):** Latest (components are vendored)
    -   **Purpose/Role in Project:** UI component library providing pre-built, customizable components (e.g., Table, Dialog, Button, Input, Select, Textarea) built with Tailwind CSS and Radix UI.
    -   **Rationale/Decision Date:** Accelerates UI development, provides accessible and well-styled components that are easily themeable. Components are added directly to the codebase (in `frontend/src/components/ui/`) allowing full control. (Decision: ~20.5.2025)

-   **Technology Name:** lucide-react
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** Provides a comprehensive set of SVG icons used throughout the frontend (e.g., PlusCircle, Edit, Trash).
    -   **Rationale/Decision Date:** Lightweight, highly customizable, and extensive icon library. (Decision: ~20.5.2025)

### Backend Technologies

-   **Technology Name:** Python
    -   **Current/Proposed Version(s):** Latest stable (e.g., ^3.10+)
    -   **Purpose/Role in Project:** Primary language for the backend logic and tool implementation.
    -   **Rationale/Decision Date:** Excellent for web development (with FastAPI), strong NLP/data processing libraries, and widely known. (Decision: 17.5.2025)

-   **Technology Name:** FastAPI
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** High-performance web framework for building the backend API.
    -   **Rationale/Decision Date:** Chosen for its speed, ease of use, automatic data validation and serialization (Pydantic), and excellent documentation. (Decision: 17.5.2025)

### Database

-   **Technology Name:** SQLite
    -   **Current/Proposed Version(s):** Version bundled with Python
    -   **Purpose/Role in Project:** Primary local data storage for tool outputs, user notes (future), etc.
    -   **Rationale/Decision Date:** Serverless, zero-configuration, single-file database, good Python support. (Decision: 17.5.2025 - see `docs/adr/ADR-001-database-choice.md`)
    -   **Key Libraries/Plugins Used (ORM, drivers):** SQLAlchemy, Alembic (for migrations)

### Optional Integrations (User-Configured)

-   **Technology Name:** Google Sheets API
    -   **Current/Proposed Version(s):** Google API Client Library for Python
    -   **Purpose/Role in Project:** Optional two-way synchronization of specific data between the local SQLite database and a user's Google Sheets.
    -   **Rationale/Decision Date:** To provide users with the flexibility to manage and access their job search data from anywhere. This is an optional feature requiring user authentication. (Decision: 17.5.2025)

### DevOps / Infrastructure

-   **Technology Name:** Local Machine
    -   **Current/Proposed Version(s):** N/A
    -   **Purpose/Role in Project:** The application is designed to run entirely locally. No external hosting or deployment infrastructure is planned for the core application.
    -   **Rationale/Decision Date:** Core project goal is privacy and local operation. (Decision: 17.5.2025)

### Testing

-   **Technology Name:** Pytest
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** Backend unit and integration testing.
    -   **Rationale/Decision Date:** Popular, powerful, and easy-to-use testing framework for Python. (Decision: 17.5.2025)

-   **Technology Name:** Jest & React Testing Library
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** Frontend component and unit testing.
    -   **Rationale/Decision Date:** Standard for React testing, good integration with Jest. (Decision: 17.5.2025)


### Linters & Formatters

-   **Technology Name:** Ruff
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** Python code formatting and linting (combines capabilities of tools like Black and Flake8).
    -   **Rationale/Decision Date:** Fast, comprehensive linter and formatter for Python. (Decision: 17.5.2025)

-   **Technology Name:** ESLint & Prettier
    -   **Current/Proposed Version(s):** Latest stable
    -   **Purpose/Role in Project:** JavaScript/TypeScript code linting and formatting for the frontend.
    -   **Rationale/Decision Date:** Industry standard for JavaScript/TypeScript linting. (Decision: 17.5.2025)


---

## 5. Dependency Versioning Strategy

*   **Proposed Default:** Use `^` (caret) for minor updates for most dependencies in `pyproject.toml` (Python/Poetry) and `package.json` (Node.js).
*   **Critical Dependencies to Pin (if any):** None identified at this stage.

---

## 6. Alternatives Considered

*   For Database: See `docs/adr/ADR-001-database-choice.md`.
*   Other alternatives for frontend/backend frameworks were implicitly considered but the user specified the core choices (FastAPI, Next.js).

---

## 7. Risks & Mitigation

*   **Risk 1:** Complexity of Google Sheets two-way sync.
    *   **Mitigation:** Implement as an entirely optional module. Thoroughly test authentication and data mapping. Provide clear user documentation.
*   **Risk 2:** Ensuring tools in the `backend/tools/` directory are truly modular and easy to add.
    *   **Mitigation:** Define a clear interface/plugin structure for tools early in the backend design.

---

## 8. Open Questions / Areas for Discussion

*   Specific UI components from Shadcn/UI to utilize for core layout and tool interfaces.
*   Detailed configuration for Ruff (e.g., specific rules to enable/disable).

---

## 9. Next Steps

*   Review and approve this initial tech stack.
*   Proceed with setting up the project structure and initial boilerplate for frontend and backend.
