# ADR-001: Choice of Local Database

**Date:** 17.5.2025 

**Status:** Accepted

## Context

The "job-hunt" application requires a local data storage solution to persist outputs from its various tools (e.g., keyword analysis results, company research notes), user preferences (if any in the future), and potentially other application-specific data. Key requirements for the database are:

*   **Local Operation:** Must run locally without requiring a separate server process.
*   **Privacy:** Data should remain on the user's machine.
*   **Ease of Use:** Simple to integrate with a Python/FastAPI backend.
*   **Sufficient Performance:** Adequately performant for a single-user desktop application.
*   **Structured Data:** Ability to store structured data efficiently.
*   **Google Sheets Sync:** While the primary storage is local, data should be structured in a way that facilitates optional two-way synchronization with Google Sheets.

## Decision Drivers

*   Simplicity of setup and maintenance for local use.
*   Robustness for a local, single-user application.
*   Good integration with the chosen backend technology (Python/FastAPI via SQLAlchemy).
*   Ability to handle structured data and relationships.
*   Low resource footprint and no external dependencies for core database functionality.

## Chosen Option: SQLite

**SQLite** is chosen as the primary local database solution for the "job-hunt" application, to be interacted with via SQLAlchemy and managed with Alembic for migrations.

## Rationale for SQLite

*   **Simplicity & Robustness:** SQLite provides an excellent balance of features, reliability, and ease of use for a local application. It's serverless and requires no complex setup.
*   **Python/FastAPI Integration:** Excellent libraries (Python's built-in `sqlite3`) and ORM support (SQLAlchemy) make integration straightforward and align with the backend rule best practices.
*   **Structured Data & Migrations:** It's a relational database capable of handling structured data. Alembic can be used for schema migrations, ensuring an organized evolution of the database structure.
*   **Performance:** More than adequate for a single-user local application.
*   **Local First & Privacy:** Aligns perfectly with the project goal of being a local application with data stored on the user's machine.
*   **Google Sheets Sync:** Relational data from SQLite can be readily transformed into a tabular format suitable for synchronization with Google Sheets.

## Considered Alternatives

1.  **Supabase (Backend-as-a-Service Platform):**
    *   **Pros:** Offers a managed PostgreSQL database, integrated authentication, storage, real-time capabilities, and a Python client library. Could accelerate development of cloud-connected features and offers good scalability if the project were to move beyond a purely local scope.
    *   **Cons for Current Project Scope:**
        *   **External Dependency:** Requires an internet connection to a Supabase project, deviating from the core "fully local" requirement for the primary database.
        *   **Complexity for Local-Only:** Adds setup complexity (Supabase project creation, API key management) if the primary goal is a simple local database.
        *   **Tooling Mismatch:** The `mcp_supabase_*` tools are designed for Supabase BaaS, not direct local SQLite interaction.
    *   **Conclusion:** While powerful, Supabase BaaS is not aligned with the immediate requirement for a simple, fully local database. It remains an interesting option for future consideration if the project scope expands to include significant cloud-based features or user accounts.

2.  **JSON Files / Flat Files (CSV, YAML):**
    *   Pros: Extremely simple for basic data, human-readable (JSON/YAML).
    *   Cons: Inefficient for querying/updating, managing data integrity and relationships is manual.

3.  **TinyDB:**
    *   Pros: Lightweight document DB, pure Python, stores data in JSON.
    *   Cons: Performance concerns with larger datasets or complex queries compared to SQLite.

4.  **DuckDB:**
    *   Pros: Fast analytical queries, can query various file formats directly.
    *   Cons: Potentially overkill for primary transactional storage; more OLAP-focused for this application's needs.

## Consequences of Choosing SQLite

*   The application will have a dependency on SQLite (which is built into Python).
*   SQLAlchemy will be used as the ORM for database interaction, and Alembic for migrations.
*   Data will be stored in a single `.sqlite` file in the `backend` directory (e.g., `backend/job_hunt.db`), making it portable and easy to back up.
*   All core database operations will be local and not require an internet connection. 