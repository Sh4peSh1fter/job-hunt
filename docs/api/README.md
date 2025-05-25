# Backend API Documentation

This section provides detailed documentation for the backend API endpoints of the Job Hunt application.

The backend is built using FastAPI and provides RESTful APIs for managing core data entities.

## Base URL

The base URL for all API v1 endpoints is `http://localhost:8000/api/v1`.

## Available APIs

Detailed documentation for each entity's API can be found in the following files:

-   [Companies API](./companies-api.md)
-   [Job Applications API](./job-applications-api.md)
-   [Job Sources API](./job-sources-api.md)
-   [Application Events API](./application-events-api.md) (Placeholder, if needed)

## Authentication

Currently, the API endpoints are not protected by authentication, aside from CORS policies restricting access to `http://localhost:3000` (the frontend development server).

## General Conventions

-   **HTTP Methods:** Standard HTTP methods are used (`GET`, `POST`, `PUT`, `DELETE`).
-   **Data Format:** Requests and responses are in JSON format.
-   **Error Handling:** Errors are typically returned with appropriate HTTP status codes and a JSON body containing a `detail` field with more information.
-   **ID fields:** All entities use an auto-incrementing integer `id` as their primary key.
-   **Timestamps:** `created_at` and `updated_at` fields are automatically managed for most entities.

For details on Pydantic schemas used for requests and responses, please refer to the [Data Models documentation](../data-models/). 