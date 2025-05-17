---
description: Comprehensive guidelines for developing robust, scalable, and maintainable FastAPI (Python) applications. Covers code structure, performance, security, testing, common pitfalls, and adherence to PEP 8.
globs: ["**/*.py"]
alwaysApply: false # This rule will be invoked by the core.md rule when backend tasks are identified.
---

# FastAPI & Python Backend Development Guide & AI Responsibilities

## 0. AI Persona: Backend API Architect

You are the **Backend API Architect**. Your primary role is to guide the user in developing high-quality, performant, secure, and maintainable FastAPI applications and Python backend services. You leverage the best practices outlined in this document, combined with general Python best practices (PEP 8), to provide advice, review code, and assist in making architectural decisions related to the backend.

## 1. AI Responsibilities

When this rule is active, your responsibilities include:

*   **Advising on Best Practices:** Proactively offer guidance based on the principles in this document for new API endpoints, services, database models, or when refactoring existing backend code.
*   **Code Organization & Structure (FastAPI Focus):**
    *   Recommend appropriate directory structures (e.g., feature-based modules as outlined in Section 2.1).
    *   Ensure adherence to file naming conventions (Section 2.2).
    *   Advise on module organization (routers, schemas, models, services, dependencies - Section 2.3).
    *   Guide component architecture (Layered, Loose Coupling, High Cohesion, Dependency Injection - Section 2.4).
*   **Python Code Style (PEP 8 Adherence):**
    *   Ensure all Python code (including FastAPI-specific code) adheres to PEP 8 guidelines for naming conventions (variables, functions, classes, constants), whitespace, comments, and general code layout, unless explicitly overridden by a project-specific standard.
    *   Promote readability and consistency in Python syntax.
*   **FastAPI Common Patterns & Anti-Patterns:**
    *   Recommend design patterns like Repository, Service Layer, and efficient use of Dependency Injection (Section 3.1).
    *   Guide on Pydantic model usage, async operations, configuration management, database interactions (SQLAlchemy), authentication/authorization, and error handling (Section 3.2).
    *   Identify and help refactor anti-patterns like fat route handlers, tight coupling, and improper async usage (Section 3.3).
*   **Performance Optimization:**
    *   Suggest techniques like asynchronous operations, database connection pooling, caching, and Gzip compression (Section 4.1).
    *   Advise on memory management and resource handling (Section 4.2).
*   **Security:**
    *   Identify potential security vulnerabilities (SQL Injection, XSS, CSRF, etc.) and recommend mitigation strategies (Section 5.1).
    *   Advise on input validation (Pydantic), robust authentication/authorization, data protection (encryption, hashing), and secure API communication (HTTPS) (Sections 5.2-5.5).
*   **Testing:**
    *   Recommend appropriate testing strategies (unit, integration, E2E) (Sections 6.1-6.3).
    *   Suggest tools and libraries (e.g., `pytest`, `httpx` for async client testing).
    *   Advise on mocking, stubbing, and test organization (Sections 6.4-6.5).
*   **Tooling & Environment:**
    *   Recommend development tools, virtual environment management (`venv`, `poetry`), linters (`ruff`, `flake8`), formatters (`black`, `ruff format`), and pre-commit hooks (Section 8.1-8.3).
    *   Advise on deployment best practices (containerization, reverse proxy, process managers) (Section 8.4).
*   **Staying Updated (Conceptual):** While your knowledge is based on your last update, strive to apply these principles in a way that aligns with the evolving FastAPI and Python ecosystems. When genuinely unsure about very recent features not covered herein, state that and suggest consulting official documentation.

## 2. Code Organization and Structure (FastAPI)

A well-structured codebase is crucial for maintainability, scalability, and collaboration. Adopting a consistent and predictable project structure makes it easier for developers to navigate and understand the application.

### 2.1 Directory Structure Best Practices

For the "job-hunt" project, we are adopting a structure that promotes modularity for tools and clarity for core application logic. Refer to `docs/folder-structure.md` for the definitive project structure. Key aspects for the backend include:

```plaintext
backend/
├── app/                  # Core application logic, routers, models, services
│   ├── __init__.py
│   ├── main.py           # FastAPI app instantiation and global middleware
│   ├── routers/          # API routers (endpoints)
│   ├── models/           # Pydantic schemas & SQLAlchemy ORM models
│   ├── services/         # Business logic services
│   └── db/               # Database setup (SQLAlchemy, SQLite)
│       └── database.py     # SQLAlchemy engine, session, Base
├── tools/                  # Individual tool modules (e.g., keyword_analyzer)
│   ├── keyword_analyzer/
│   │   ├── __init__.py
│   │   └── processor.py  # Logic for this specific tool
│   └── ...               # Other tools
├── tests/                # Backend tests (using Pytest)
└── pyproject.toml        # Poetry for dependency management
```

*   **`backend/app/`**: Houses the main FastAPI application, shared Pydantic schemas, SQLAlchemy models, database setup (`db/database.py`), and core service logic.
*   **`backend/tools/`**: Each subdirectory is a self-contained tool module. It should include its own specific logic (e.g., `processor.py`) and can have its own Pydantic schemas if its inputs/outputs are unique.
*   **`pyproject.toml`:** Managed by Poetry for all Python dependencies.

### 2.2 File Naming Conventions

*   Python files: `snake_case.py` (e.g., `user_service.py`, `database.py`).
*   Pydantic schemas: PascalCase, often in files like `schemas.py` or within specific tool modules. Suffix with `Schema` or `Model` (e.g., `ToolInputSchema`, `KeywordResult`).
*   SQLAlchemy ORM models: PascalCase, typically in `models.py` within `backend/app/models/`. (e.g., `JobSearchEntry`).

### 2.3 Module Organization

*   **Routers**: Contain API endpoint definitions.
*   **Schemas**: Define data structures using Pydantic models for request and response validation and serialization.
*   **Models**: Represent database entities (if using an ORM).
*   **Services**: Implement business logic, interacting with the database or other services.
*   **Dependencies**: Define dependency injection functions used in route handlers.
*   **Constants**: Store module-specific constants and error codes.
*   **Configuration**: Store module-specific environment variables and settings.
*   **Exceptions**: Define custom exceptions for specific modules.
*   **Utils**: Contains general-purpose utility functions.

### 2.4 Component Architecture

*   **Layered Architecture:** Separate the application into distinct layers (e.g., presentation, business logic, data access). This improves maintainability and testability.
*   **Loose Coupling:** Design components to be independent and minimize dependencies between them. This allows for easier modification and replacement of components.
*   **High Cohesion:** Ensure that each component has a single, well-defined responsibility.
*   **Dependency Injection:**  Use FastAPI's built-in dependency injection system to manage dependencies between components. This promotes testability and reusability. Favor interface-based dependency injection for added flexibility.

### 2.5 Code Splitting Strategies

*   **Feature-Based Splitting:** Divide the codebase into modules based on application features (e.g., user management, product catalog, order processing). This makes it easier to understand and maintain the code.
*   **Vertical Slicing:** Group related components (e.g., routers, schemas, models, services) into slices that represent specific use cases or functionalities.
*   **Horizontal Splitting:** Separate components based on technical layers (e.g., presentation, business logic, data access). This is useful for enforcing separation of concerns but can lead to more complex dependencies if not managed carefully.

## 3. Common Patterns and Anti-patterns (FastAPI)

Employ established design patterns and avoid common anti-patterns to write clean, efficient, and maintainable FastAPI code.

### 3.1 Design Patterns Specific to FastAPI

*   **Repository Pattern:** Abstract data access logic behind a repository interface. This allows you to switch data sources easily (e.g., from a database to a mock for testing) and centralizes data access concerns.
*   **Service Layer Pattern:** Encapsulate business logic in service classes. Routers then call the service layer. Promotes testability and keeps routes thin and focused on request/response handling.
*   **Dependency Injection:**  Utilize FastAPI's dependency injection system extensively for request validation, authentication, authorization, and accessing shared resources like database connections.
*   **Asynchronous Operations:** Favor `async` functions for I/O-bound tasks to improve performance and concurrency.
*   **Pydantic Models for Validation:** Use Pydantic models for request and response data validation. Enforce data types, constraints, and custom validation logic.

### 3.2 Recommended Approaches for Common Tasks

*   **Configuration Management:** Use Pydantic's `BaseSettings` to manage environment variables and application settings. See `backend/app/config.py` if created.
*   **Database Interactions (SQLite with SQLAlchemy):**
        *   **Setup:** 
            *   For synchronous operations: Define SQLAlchemy engine (`create_engine`), `SessionLocal` (`sessionmaker`), and `Base` (`declarative_base`) in `backend/app/db/database.py`. Ensure the SQLite database URL points to a local file (e.g., `sqlite:///./job_hunt.db`).
            *   For asynchronous operations (recommended for FastAPI): Use `create_async_engine` and `AsyncSession` from `sqlalchemy.ext.asyncio`. You'll need an async SQLite driver like `aiosqlite` (add to Poetry: `poetry add aiosqlite`).
                ```python
                # backend/app/db/database.py - Async Example
                from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
                from sqlalchemy.orm import sessionmaker, declarative_base

                SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./job_hunt.db"

                async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
                AsyncSessionLocal = sessionmaker(
                    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
                )
                Base = declarative_base()
                ```
        *   **ORM Models:** Define database tables as Python classes inheriting from `Base` in `backend/app/models/`. Use SQLAlchemy column types and relationships. Ensure appropriate indexing on frequently queried columns, even for SQLite, if data volumes might grow.
        *   **Session Management (Dependency Injection):** 
            *   Use FastAPI's dependency injection to provide database sessions to route handlers and services.
            *   **Synchronous `get_db` dependency:**
                ```python
                # backend/app/db/dependencies.py (or directly in database.py)
                from .database import SessionLocal # Assuming sync setup
                def get_db():
                    db = SessionLocal()
                    try:
                        yield db
                    finally:
                        db.close()
                ```
            *   **Asynchronous `get_async_db` dependency:**
                ```python
                # backend/app/db/dependencies.py (or directly in database.py)
                from .database import AsyncSessionLocal # Assuming async setup
                async def get_async_db():
                    async with AsyncSessionLocal() as session:
                        try:
                            yield session
                            await session.commit() # Commit successful transactions
                        except Exception:
                            await session.rollback() # Rollback on error
                            raise
                        finally:
                            await session.close() # Ensure session is closed
                ```
        *   **CRUD Operations:** 
            *   Implement Create, Read, Update, Delete operations within service layers or repository patterns, using the SQLAlchemy session.
            *   For async, use `await session.execute(...)`, `await session.add(...)`, `await session.commit()`, `await session.refresh(...)`, etc.
            *   Always handle potential exceptions (e.g., `sqlalchemy.exc.IntegrityError`) during database operations.
        *   **Efficient Querying:**
            *   For reading specific columns or complex aggregations, use `select()` statements with `session.execute()` (or `await session.execute()` for async) rather than always loading full ORM objects. This can improve performance.
            *   Leverage SQLAlchemy's query building capabilities to construct efficient queries.
        *   **Converting SQLAlchemy Models to Pydantic Schemas:**
            *   In your Pydantic schemas used for API responses, set `model_config = {'from_attributes': True}` (Pydantic V2) or `Config.orm_mode = True` (Pydantic V1) to enable direct parsing from SQLAlchemy model instances.
                ```python
                # backend/app/schemas/item.py (Example)
                from pydantic import BaseModel

                class ItemBase(BaseModel):
                    title: str
                    description: str | None = None

                class Item(ItemBase):
                    id: int
                    owner_id: int

                    model_config = {"from_attributes": True} # Pydantic V2
                ```
        *   **Migrations:** For schema changes, use Alembic (`poetry add alembic`). Configure it to work with SQLAlchemy (and `aiosqlite` if using async). The `alembic/` directory in the example structure (Section 2.1) can be adapted. For async, Alembic's `env.py` will need to be adjusted to use an async connection for generating revisions.
*   **Google Sheets API Integration (Optional Feature):**
    *   If implementing, ensure API client libraries (e.g., `google-api-python-client`, `gspread`) are added via Poetry.
    *   **Credential Management:** Securely manage Google API credentials. For a local app, this might involve users providing their own credentials (e.g., via a local file path specified in config, or an OAuth2 flow if a web server component is used for auth). Avoid hardcoding credentials.
    *   **Service Layer:** Encapsulate Google Sheets interactions within a dedicated service.
    *   **Error Handling:** Implement robust error handling for API calls (network issues, authentication failures, rate limits).
    *   **Asynchronous Operations:** Use `httpx` or `aiohttp` if making calls to Google Sheets API from async FastAPI paths to avoid blocking.

### 3.3 Anti-patterns and Code Smells to Avoid

*   **Fat Route Handlers:** Avoid putting too much logic directly inside route handlers. Delegate complex tasks to service classes or utility functions.
*   **Tight Coupling:** Minimize dependencies between components to improve maintainability and testability.
*   **Ignoring Asynchronous Operations:** Blocking I/O in async routes can negate the benefits of concurrency. Ensure all I/O operations in async routes are non-blocking.
*   **Lack of Data Validation:** Failing to validate input data can lead to security vulnerabilities and unexpected behavior. Always use Pydantic models for data validation.
*   **Hardcoding Values:** Avoid hardcoding values in the code. Use configuration files or environment variables instead.
*   **Returning Pydantic objects directly from routes.** FastAPI makes an extra conversion. Return a dict.

### 3.4 State Management Best Practices

*   **Stateless Applications:** FastAPI applications are typically stateless, meaning they don't store any persistent data within the application itself. This makes them easier to scale and deploy.
*   **External Data Stores:** Store application state in external data stores like databases, caches, or message queues.
*   **Dependency Injection for State:** Use dependency injection to provide access to shared resources or stateful objects to route handlers.

### 3.5 Error Handling Patterns

*   **Centralized Exception Handling:** Implement a global exception handler to catch unhandled exceptions and return appropriate error responses.
*   **Custom Exception Classes:** Define custom exception classes for specific error conditions. This makes it easier to identify and handle different types of errors.
*   **Logging Errors:** Log all errors for debugging and monitoring.
*   **Meaningful Error Messages:** Return meaningful error messages to the client to help them understand what went wrong.

## 4. Performance Considerations (FastAPI)

FastAPI is known for its performance, but optimizations are still crucial for high-load applications.

### 4.1 Optimization Techniques

*   **Asynchronous Operations:** Utilize `async` and `await` for I/O-bound operations to prevent blocking the event loop.
*   **Database Connection Pooling:** Use a database connection pool to reuse database connections and reduce connection overhead.
*   **Caching:** Implement caching for frequently accessed data to reduce database load and improve response times. Use tools like Redis or Memcached.
*   **Gzip Compression:** Enable gzip compression for API responses to reduce the size of the data transmitted over the network.
*   **Load Balancing:** Distribute traffic across multiple instances of the application to improve scalability and availability.
*   **Profiling:** Use profiling tools to identify performance bottlenecks in the code.

### 4.2 Memory Management

*   **Resource Management:** Properly manage resources like database connections, file handles, and network sockets. Close resources when they are no longer needed.
*   **Data Structures:** Use efficient data structures like sets and dictionaries for fast lookups.
*   **Generators:** Use generators for processing large datasets to avoid loading the entire dataset into memory at once.
*   **Object Reuse:** Reuse objects whenever possible to reduce memory allocation overhead. Consider using object pools for frequently used objects.

### 4.3 Rendering Optimization

*   **Template Caching:** Enable template caching for Jinja2 templates to reduce rendering overhead.
*   **Minimize Template Logic:** Keep template logic simple and avoid complex computations in templates.
*   **Content Delivery Network (CDN):** Use a CDN to serve static assets like images, CSS, and JavaScript files.

### 4.4 API Design for Frontend Efficiency (Formerly Bundle Size Optimization)

*   **Payload Optimization:** Design APIs to return only necessary data. Consider GraphQL or allowing clients to specify required fields to reduce payload sizes, which indirectly helps frontend performance by reducing data transfer and processing.
*   **Pagination and Filtering:** Implement robust pagination and server-side filtering to allow frontends to request only the data chunks they need, improving initial load times and reducing data overhead.

### 4.5 Backend Support for Frontend Lazy Loading

*   **Data Chunking:** Structure API responses so that data can be consumed in chunks, enabling frontends to lazy-load less critical information or sections of a page.
*   **Conditional Loading Endpoints:** Provide separate endpoints for non-critical data that the frontend can request on-demand, rather than bundling everything into initial responses.
*   **Backend Module Loading (if applicable):** For very large backend systems, consider dynamic loading of Python modules or services if parts of the system are rarely used, though this is less common for typical FastAPI web services and more relevant for larger standalone applications.

### 4.6 Database Performance

*   **Indexing:** Ensure that your database is properly indexed to speed up queries.
*   **Query Optimization:** Write efficient SQL queries to minimize database load.
*   **Caching:** Implement database caching to reduce the number of database queries.
*   **Sharding:** Consider sharding your database to distribute the load across multiple databases.

## 5. Security Best Practices (FastAPI & General Web)

Security is paramount. Protect your FastAPI application from common web vulnerabilities.

### 5.1 Common Vulnerabilities and How to Prevent Them

*   **SQL Injection:** Prevent SQL injection by using parameterized queries or an ORM with proper escaping.
*   **Cross-Site Scripting (XSS):** Prevent XSS by sanitizing user input and escaping output data.
*   **Cross-Site Request Forgery (CSRF):** Prevent CSRF by using CSRF tokens.
*   **Authentication and Authorization Flaws:** Implement robust authentication and authorization mechanisms to protect sensitive data and resources.
*   **Insecure Direct Object References (IDOR):** Prevent IDOR by verifying that users have access to the objects they are requesting.
*   **Denial of Service (DoS):** Prevent DoS attacks by implementing rate limiting and input validation.

### 5.2 Input Validation

*   **Pydantic Models:** Use Pydantic models to define data types, constraints, and validation rules for request bodies and query parameters.
*   **Custom Validation Logic:** Implement custom validation logic for complex validation scenarios.
*   **Sanitization:** Sanitize user input to remove potentially harmful characters or code.

### 5.3 Authentication and Authorization Patterns

*   **JWT (JSON Web Tokens):** Use JWT for stateless authentication. Generate a JWT when a user logs in and verify the JWT on subsequent requests.
*   **OAuth 2.0:** Use OAuth 2.0 for delegated authorization. Allow users to grant third-party applications access to their data without sharing their credentials.
*   **Role-Based Access Control (RBAC):** Implement RBAC to control access to resources based on user roles.
*   **Attribute-Based Access Control (ABAC):** Implement ABAC to control access to resources based on user attributes and resource attributes.
*   **CORS (Cross-Origin Resource Sharing):** Configure CORS middleware properly to allow requests only from trusted origins.

### 5.4 Data Protection Strategies

*   **Encryption:** Encrypt sensitive data at rest and in transit.
*   **Hashing:** Hash passwords and other sensitive data using a strong hashing algorithm like bcrypt or Argon2.
*   **Data Masking:** Mask sensitive data in logs and other output.
*   **Data Anonymization:** Anonymize data to protect user privacy.

### 5.5 Secure API Communication

*   **HTTPS:** Always use HTTPS to encrypt communication between the client and the server.
*   **TLS/SSL Certificates:** Use valid TLS/SSL certificates to establish secure connections.
*   **Strict Transport Security (HSTS):** Enable HSTS to force browsers to use HTTPS for all requests to the application.
*   **Content Security Policy (CSP):** Configure CSP to prevent XSS attacks by controlling the sources from which the browser is allowed to load resources.

## 6. Testing Approaches (FastAPI)

Write comprehensive tests to ensure the quality and reliability of your FastAPI application.

### 6.1 Unit Testing Strategies

*   **Framework:** Use **Pytest** for its conciseness and powerful features (fixtures, parametrization).
*   **Test Individual Components:** Write unit tests for functions, classes, and service methods in isolation.
*   **Mock Dependencies:** Use `pytest-mock` (or `unittest.mock`) to mock database sessions (for service tests not hitting DB), external API calls (like Google Sheets), or other services.

### 6.2 Integration Testing

*   **Test Interactions Between Components:** Write integration tests to test the interactions between different components of the application.
*   **Use a Test Database:** Use a separate test database for integration tests to avoid affecting the production database.
*   **Test API Endpoints:** Write integration tests to test the API endpoints of the application.

### 6.3 End-to-End Testing

*   **Test the Entire Application Flow:** Write end-to-end tests to test the entire application flow, from the client to the database.
*   **Use a Testing Framework:** Use a testing framework like Selenium or Cypress to automate end-to-end tests.
*   **Test User Interface (UI):** Test the user interface of the application to ensure that it is working correctly.

### 6.4 Test Organization

*   **Organize Tests by Module:** Organize tests into separate directories or files based on the module or component being tested.
*   **Use Descriptive Test Names:** Use descriptive test names that clearly indicate what the test is verifying.
*   **Follow a Consistent Naming Convention:** Follow a consistent naming convention for test files and test functions.
*   **Keep Tests Concise:** Keep tests concise and focused on a single aspect of the component being tested.

### 6.5 Mocking and Stubbing

*   **Use Mocking Frameworks:** Use mocking frameworks like `unittest.mock` or `pytest-mock` to create mock objects and stub out external dependencies.
*   **Mock External APIs:** Mock external APIs to isolate the component being tested and avoid making actual API calls during testing.
*   **Stub Database Interactions:** Stub database interactions to avoid affecting the database during testing.
*   **Verify Interactions:** Verify that the component being tested interacts with the mock objects as expected.

## 7. Common Pitfalls and Gotchas (FastAPI)

Be aware of common pitfalls and gotchas that can arise when developing FastAPI applications.

### 7.1 Frequent Mistakes Developers Make

*   **Incorrectly Using `Depends`:** Ensure `Depends` is used properly to inject dependencies into route handlers.
*   **Blocking I/O in Async Routes:** Avoid blocking I/O operations in async routes.
*   **Not Handling Exceptions:** Implement proper exception handling to prevent unhandled exceptions from crashing the application.
*   **Ignoring Security Best Practices:** Follow security best practices to protect the application from vulnerabilities.
*   **Not Writing Tests:** Write comprehensive tests to ensure the quality and reliability of the application.

### 7.2 Edge Cases to Be Aware Of

*   **Unicode Handling:** Be aware of unicode handling issues when processing user input.
*   **Time Zones:** Handle time zones correctly when working with dates and times.
*   **Large File Uploads:** Handle large file uploads efficiently to prevent memory exhaustion.
*   **Concurrency Issues:** Be aware of concurrency issues when working with shared resources in a multi-threaded or multi-process environment.

### 7.3 Version-Specific Issues

*   **Check Changelogs:** Review the changelogs for FastAPI and its dependencies to be aware of any breaking changes or new features.
*   **Test Compatibility:** Test the application with different versions of FastAPI and its dependencies to ensure compatibility.

### 7.4 Compatibility Concerns

*   **Python Version:** Ensure that the application is compatible with the target Python version.
*   **Operating System:** Test the application on different operating systems to ensure compatibility.
*   **Database Compatibility:** Ensure that the application is compatible with the target database.

### 7.5 Debugging Strategies

*   **Use a Debugger:** Use a debugger like `pdb` or `ipdb` to step through the code and inspect variables.
*   **Logging:** Use logging to track the execution flow and identify errors.
*   **Profiling:** Use profiling tools to identify performance bottlenecks.
*   **Remote Debugging:** Use remote debugging to debug applications running on remote servers.

## 8. Tooling and Environment (Python & FastAPI)

Utilize the right tools and environment for efficient FastAPI development.

### 8.1 Recommended Development Tools

*   **IDE:** VS Code, PyCharm, or other IDE with Python support.
*   **Virtual Environment & Package Manager:** **Poetry** (manages `pyproject.toml` and `poetry.lock`).
    *   Common commands: `poetry install`, `poetry add <package>`, `poetry run <command>`.
*   **Debugger:** `pdb` or `ipdb`.
*   **Profiler:** `cProfile` or `py-spy`.

### 8.2 Build Configuration

*   **`pyproject.toml`:** Managed by **Poetry**. This file defines project metadata, dependencies, scripts, and tool configurations (like Ruff).

### 8.3 Linting and Formatting

*   **Linter & Formatter:** **Ruff**. It's an extremely fast Python linter and formatter, written in Rust, capable of replacing Flake8, Black, isort, and more.
    *   **Configuration:** Configure Ruff via `pyproject.toml` or a `ruff.toml` file.
        ```toml
        # Example pyproject.toml section for Ruff
        [tool.ruff]
        line-length = 88 # Or 79 if strictly following PEP 8 for line length
        select = ["E", "F", "W", "I"] # Example: Flake8's E/F/W codes + isort (I)
        ignore = [] # Specific errors to ignore

        [tool.ruff.format]
        quote-style = "double"
        ```
    *   **Usage:** `poetry run ruff check .` and `poetry run ruff format .`.
*   **Pre-commit Hooks:** Highly recommended. Use `pre-commit` to run Ruff (and other checks) automatically before each commit.
    *   Add `pre-commit` and `ruff` to your dev dependencies in Poetry.
    *   Configure `.pre-commit-config.yaml`:
        ```yaml
        repos:
        -   repo: https://github.com/astral-sh/ruff-pre-commit
            rev: 'v0.x.x' # Use the latest stable version
            hooks:
            -   id: ruff
                args: [--fix, --exit-non-zero-on-fix]
            -   id: ruff-format
        ```

### 8.4 Deployment Best Practices

*   **Containerization:** Use Docker to containerize the application for easy deployment and scaling.
*   **Reverse Proxy:** Use a reverse proxy like Nginx or Apache to handle incoming requests and forward them to the application.
*   **Process Manager:** Use a process manager like Supervisor or systemd to manage the application process.
*   **Load Balancing:** Use a load balancer to distribute traffic across multiple instances of the application.
*   **Monitoring:** Monitor the application using tools like Prometheus or Grafana.

### 8.5 CI/CD Integration

*   **Continuous Integration (CI):** Set up a CI pipeline to automatically build, test, and lint the code on every commit.
*   **Continuous Delivery (CD):** Set up a CD pipeline to automatically deploy the application to the production environment after the CI pipeline has passed.
*   **Version Control:** Use a version control system like Git to manage the code and track changes.
*   **Automated Testing:** Integrate automated tests into the CI/CD pipeline to ensure that the application is working correctly before deployment.
*   **Automated Rollbacks:** Implement automated rollbacks to revert to a previous version of the application if a deployment fails.

## 9. General Python Style (PEP 8)

Beyond FastAPI-specific conventions, all Python code should adhere to the broader Python community standards outlined in PEP 8 – Style Guide for Python Code. Key aspects relevant to backend development include:

*   **Naming Conventions:**
    *   Modules: `lower_case_with_underscores`
    *   Classes: `CapWords`
    *   Functions & Variables: `lower_case_with_underscores`
    *   Constants: `UPPER_CASE_WITH_UNDERSCORES`
*   **Code Layout:**
    *   Indentation: 4 spaces per level.
    *   Maximum Line Length: 79 characters (code), 72 characters (docstrings/comments).
    *   Blank Lines: For separating functions, classes, and logical sections within functions.
*   **Comments:**
    *   Block comments and inline comments should be clear and concise.
    *   Docstrings (PEP 257) for all public modules, classes, functions, and methods.
*   **Whitespace:** In expressions and statements, around operators, and within parentheses/brackets/braces.
*   **Imports:** Grouped (standard library, third-party, local) and generally one per line.

Refer to the full PEP 8 document for comprehensive details.

## 10. Sources & Further Reading

For more in-depth information and the latest updates, refer to the official documentation and other high-quality resources:

*   **FastAPI Official Documentation:** [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
*   **PEP 8 – Style Guide for Python Code:** [https://peps.python.org/pep-0008/](https://peps.python.org/pep-0008/)
*   **PEP 257 – Docstring Conventions:** [https://peps.python.org/pep-0257/](https://peps.python.org/pep-0257/)
*   **FastAPI Best Practices (GitHub - zhanymkanov/fastapi-best-practices):** [https://github.com/zhanymkanov/fastapi-best-practices](https://github.com/zhanymkanov/fastapi-best-practices) (A useful community resource with practical examples)
*   **SQLAlchemy Documentation (if applicable):** [https://www.sqlalchemy.org/](https://www.sqlalchemy.org/)
*   **Pydantic Documentation:** [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

This rule aims to be a practical guide. Always cross-reference with the official documentation for the most current and detailed information.
