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

*   Simplicity of setup and maintenance.
*   Robustness for a local, single-user application.
*   Good integration with the chosen backend technology (Python/FastAPI).
*   Ability to handle structured data and relationships if needed for future features.
*   Low resource footprint.

## Considered Options

1.  **SQLite:**
    *   Pros: Serverless, zero-configuration, single-file database, excellent Python support, mature, ACID compliant.
    *   Cons: Less feature-rich than client-server RDBMS (not a major issue for this use case).

2.  **JSON Files / Flat Files (CSV, YAML):**
    *   Pros: Extremely simple for basic data, human-readable (JSON/YAML).
    *   Cons: Inefficient for querying/updating, managing data integrity and relationships is manual, concurrency issues (less relevant here).

3.  **TinyDB:**
    *   Pros: Lightweight document DB, pure Python, stores data in JSON.
    *   Cons: Performance concerns with larger datasets or complex queries compared to SQLite.

4.  **DuckDB:**
    *   Pros: Fast analytical queries, can query various file formats directly.
    *   Cons: Potentially overkill for primary transactional storage; more OLAP-focused.

## Decision

**SQLite** is chosen as the primary local database solution for the "job-hunt" application.

## Rationale

*   **Simplicity & Robustness:** SQLite provides a good balance of features, reliability, and ease of use for a local application. It's serverless and requires no complex setup.
*   **Python/FastAPI Integration:** Excellent libraries and ORM support (like SQLAlchemy with FastAPI) make integration straightforward.
*   **Structured Data:** It's a relational database, capable of handling structured data and relationships, which will be beneficial for storing tool outputs and potential future features like tracking job applications.
*   **Performance:** More than adequate for a single-user local application.
*   **Google Sheets Sync:** Relational data from SQLite can be readily transformed into a tabular format suitable for synchronization with Google Sheets.

While flat files are simpler for very basic needs, they lack the querying and data integrity features that SQLite offers. TinyDB is a good lightweight option but SQLite provides more robust relational capabilities. DuckDB is powerful but more suited for analytical workloads rather than the primary application database in this context.

## Consequences

*   The application will have a dependency on SQLite (which is built into Python, so no external installation is usually needed).
*   Data will be stored in a single `.sqlite` file, making it portable and easy to back up.
*   Development will involve choosing an appropriate way to interact with SQLite (e.g., SQLAlchemy ORM, or direct SQL queries via `sqlite3` module). 