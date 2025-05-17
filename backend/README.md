# Backend

This directory contains the FastAPI backend application for the Job Hunt project.

## Initial Setup

1.  **Navigate to this `backend` directory.**
2.  **Ensure Python 3.10+ and Poetry are installed.**
3.  **Create a virtual environment and install dependencies:**
    ```bash
    poetry install
    ```
    *(This replaces manual venv creation and pip install steps, as Poetry handles it.)*

    If you don't have poetry and want to install it in the virtual environment of this project itself:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install poetry
    poetry init
    ```

## Running the Development Server

Once the setup is complete and dependencies are installed, you can run the FastAPI development server using Uvicorn:

1.  **Ensure your terminal is in the `job-hunt/backend` directory.**
2.  **Run the server:**
    ```bash
    poetry run uvicorn app.main:app --reload --app-dir .
    ```
    *   `app.main:app`: Points to the `app` instance in `backend/app/main.py`.
    *   `--reload`: Enables auto-reloading when code changes are detected.
    *   `--app-dir .`: Specifies that the application directory (where `app/` can be found) is the current directory (`backend/`).

3.  **The server will typically be available at `http://127.0.0.1:8000`.**
    *   Health Check: `http://127.0.0.1:8000/health`
    *   API Docs (Swagger UI): `http://127.0.0.1:8000/docs`
    *   Alternative API Docs (ReDoc): `http://127.0.0.1:8000/redoc`

## Project Structure

Refer to `docs/folder-structure.md` in the main project documentation for a detailed overview of the backend structure.

## Dependencies

Dependencies are managed by Poetry and are listed in `pyproject.toml`.

## Linting and Formatting

This project uses Ruff for linting and formatting. Configure in `pyproject.toml`.

*   Check code:
    ```bash
    poetry run ruff check .
    ```
*   Format code:
    ```bash
    poetry run ruff format .
    ```

## Migrations

Database migrations are handled by Alembic. After configuring `alembic.ini` and `alembic/env.py`, you can use the following commands from the `job-hunt/backend` directory:

*   **Create a new migration script (after making changes to your SQLAlchemy models in `app/models/`):**
    ```bash
    poetry run alembic revision -m "create_some_table" --autogenerate
    ```
    Replace `"create_some_table"` with a descriptive message for your migration.

*   **Apply pending migrations to the database:**
    ```bash
    poetry run alembic upgrade head
    ```

*   **Downgrade to a previous migration:**
    ```bash
    poetry run alembic downgrade -1  # Downgrade by one revision
    # or poetry run alembic downgrade <revision_id>
    ```

*   **Check current database revision:**
    ```bash
    poetry run alembic current
    ```

*   **View migration history:**
    ```bash
    poetry run alembic history
    ```

(Further instructions to be added once Alembic is fully configured).