# Product Requirements Document: job-hunt

## 1. Introduction

**Project Name:** job-hunt

**Purpose:** This document outlines the product requirements for "job-hunt," a local web application designed to assist individuals in managing and optimizing their job search process. It consolidates several focused tools into a single, easy-to-use interface to help streamline common tasks such as analyzing job descriptions, gathering company information, and managing personal search data.

**Problem Statement:** The job search process often involves a wide range of repetitive and fragmented tasks, including tailoring resumes, tracking applications, researching companies, and identifying job-specific keywords. This project aims to bring structure and automation to those efforts by providing a centralized platform that runs locally and does not require any external dependencies or data storage.

## 2. Goals

*   **Centralization:** Centralize useful utilities to support various stages of the job search process.
*   **Automation:** Automate time-consuming and repetitive tasks.
*   **Privacy:** Maintain user privacy by ensuring all functionality is local and self-hosted.
*   **Modularity & Extensibility:** Provide a modular, extensible architecture to support additional tools in the future.
*   **User Experience:** Deliver a simple and effective user experience.

## 3. Target Audience

Individuals actively engaged in a job search, including but not limited to:
*   New graduates.
*   Professionals seeking new opportunities.
*   Career changers.
*   Freelancers looking for projects.

The common characteristic is a need for tools to make the job search process more efficient and organized.

## 4. Proposed Features

### 4.1. Homepage
*   **Description:** A static landing page that provides an overview of the "job-hunt" application.
*   **Content:**
    *   Introduction to the platform.
    *   Guidance on how to use the tools effectively.
    *   Links to different sections of the application.
    *   Information about privacy and local data storage.
*   **Technology:** Served by the Next.js frontend, content managed via Markdown files.

### 4.2. Tools Section
*   **Description:** A dedicated section offering a collection of utilities. The architecture should allow for easy addition and management of new tools.
*   **General Tool Features:**
    *   Clear input mechanisms.
    *   Understandable output displays.
    *   Option to export tool outputs (e.g., to CSV, potentially Google Sheets).

#### 4.2.1. Keyword Frequency Analyzer
*   **User Story:** As a job seeker, I want to paste a job description and see the most frequent keywords, so I can better tailor my resume and understand employer priorities.
*   **Functionality:**
    *   Accepts text input (job description).
    *   Processes the text to identify and count the frequency of key terms (e.g., nouns, noun phrases, specific skills).
    *   Displays a list of keywords and their frequencies, possibly with basic filtering or visualization.
    *   Ignores common stop words.
*   **Input:** Text area for pasting job description.
*   **Output:** List of keywords and counts. Option to export.

#### 4.2.2. Company Research Assistant
*   **User Story:** As a job seeker, I want to enter a company name and get a summary of publicly available information, so I can quickly prepare for interviews or assess company fit.
*   **Functionality:**
    *   Accepts company name as input.
    *   (To be defined: What specific information should be gathered? From what sources? E.g., company website, LinkedIn, news articles. This will likely involve web scraping or API integration if available and permissible for local use without requiring user API keys initially).
    *   Presents a summarized view of the gathered information.
*   **Input:** Text field for company name.
*   **Output:** Structured information about the company. Option to export.

#### 4.2.3. Resume Tailoring Utility (Planned)
*   **User Story:** As a job seeker, I want to compare my resume content against a job description to identify areas for improvement and ensure I'm highlighting relevant skills and experiences.
*   **Functionality (High-Level):**
    *   Accepts resume text/file and job description text.
    *   Analyzes both texts to identify matching keywords, skills, and potential gaps in the resume.
    *   Provides suggestions or a score for relevance.
*   **Status:** Planned for a future iteration. Initial architecture should not preclude its addition.

## 5. User Interface and User Experience (UI/UX) Design

This section outlines the planned user interface (UI) design, user experience (UX) flow, and overall aesthetic for the "job-hunt" application.

**Last Updated:** May 19, 2024

### 5.1. Overall Look and Feel

*   **Base Inspiration:** The UI will draw inspiration from the **Tailwind Next.js Starter Blog** ([https://github.com/timlrx/tailwind-nextjs-starter-blog](https://github.com/timlrx/tailwind-nextjs-starter-blog)), adapted to suit a utility-focused application.
*   **Aesthetic:** Clean, modern, professional, and minimalist. The focus will be on usability and clarity, ensuring that users can easily access and operate the tools.
*   **Color Palette:** (To be defined - suggest a simple, professional palette. Perhaps a primary accent color with neutral grays for text and backgrounds.)
*   **Typography:** (To be defined - suggest clear, readable sans-serif fonts, potentially using `next/font` for optimization as per `frontend.md`.)
*   **Responsiveness:** The application must be responsive and provide a good user experience on desktop and tablet devices. Mobile responsiveness is a secondary concern for initial MVP but should be kept in mind for component design.

### 5.2. Navigation Structure

A persistent global header will contain the primary navigation:

*   **Header:**
    *   **Application Title/Logo (Optional):** "Job Hunt" or a simple icon on the left.
    *   **Navigation Links (Right or Center):**
        *   **"Guide"**: Links to the homepage (`/`).
        *   **"Tools"**: Links to the tools overview page (`/tools`).

### 5.3. Page Layouts and Wireframes (Text-based Descriptions)

#### 5.3.1. Global Layout

*   **Header:** Fixed or sticky at the top, containing navigation.
*   **Main Content Area:** Below the header, occupying the majority of the viewport. This area will render the content of the current page.
*   **Footer (Optional):** A small, unobtrusive footer at the bottom, possibly containing a copyright notice or version information.

#### 5.3.2. Guide Page (`/`)

*   **Purpose:** Introduction, user guide, project information.
*   **Layout:**
    *   `+------------------------------------+"`
    *   `| Header (Nav: Guide | Tools)         |"`
    *   `+------------------------------------+"`
    *   `| Page Title (e.g., "Job Hunt Guide") |"`
    *   `+------------------------------------+"`
    *   `| Main Content Area (Markdown Text)  |"`
    *   `| - Section 1                        |"`
    *   `| - Section 2                        |"`
    *   `| - ...                              |"`
    *   `+------------------------------------+"`
    *   `| Footer (Optional)                  |"`
    *   `+------------------------------------+"`
*   **Content:** Primarily text-based, rendered from Markdown. Should be easily readable with clear headings and paragraphs.

#### 5.3.3. Tools Overview Page (`/tools`)

*   **Purpose:** Display available tools and allow navigation to them.
*   **Layout:**
    *   `+------------------------------------+"`
    *   `| Header (Nav: Guide | Tools)         |"`
    *   `+------------------------------------+"`
    *   `| Page Title (e.g., "Available Tools")|"`
    *   `+------------------------------------+"`
    *   `| Tool Card Grid/List                |"`
    *   `| +-----------+  +-----------+       |"`
    *   `| | Tool 1    |  | Tool 2    |       |"`
    *   `| | (Desc)    |  | (Desc)    |       |"`
    *   `| +-----------+  +-----------+       |"`
    *   `| +-----------+  +-----------+       |"`
    *   `| | Tool 3    |  | ...       |       |"`
    *   `| | (Desc)    |  |           |       |"`
    *   `| +-----------+  +-----------+       |"`
    *   `+------------------------------------+"`
    *   `| Footer (Optional)                  |"`
    *   `+------------------------------------+"`
*   **Tool Cards:** Each card will display the tool's name, a short description, and potentially an icon. Clicking a card navigates to the tool's specific page.

#### 5.3.4. Individual Tool Page (e.g., `/tools/keyword-analyzer`)

*   **Purpose:** Provide the UI for a specific tool.
*   **Layout (Example: Keyword Analyzer):**
    *   `+------------------------------------+"`
    *   `| Header (Nav: Guide | Tools)         |"`
    *   `+------------------------------------+"`
    *   `| Page Title (e.g., "Keyword Freq.")  |"`
    *   `| Brief Instructions                 |"`
    *   `+------------------------------------+"`
    *   `| Input Area:                        |"`
    *   `| +--------------------------------+ |"`
    *   `| | Text Area for Job Desc.      | |"`
    *   `| +--------------------------------+ |"`
    *   `| [Analyze Button]                   |"`
    *   `+------------------------------------+"`
    *   `| Results Area:                      |"`
    *   `| +--------------------------------+ |"`
    *   `| | Keyword | Count | ...          | |"`
    *   `| | ---------|-------|----          | |"`
    *   `| | Word 1  | 10    |              | |"`
    *   `| | Word 2  | 8     |              | |"`
    *   `| +--------------------------------+ |"`
    *   `+------------------------------------+"`
    *   `| Footer (Optional)                  |"`
    *   `+------------------------------------+"`
*   **Content:** Specific to each tool. Must include clear input fields, action buttons, and a well-formatted results display area.

### 5.4. Key UI Components & Styling

*   **Component Library:** We will primarily use **Shadcn/UI** components ([https://ui.shadcn.com/](https://ui.shadcn.com/)) for building blocks like buttons, cards, input fields, tables, etc. This ensures a consistent look and feel and accelerates development. Custom components specific to a tool's unique needs will be built by composing Shadcn/UI elements or from scratch if necessary.
*   **Styling:** **Tailwind CSS** will be the primary styling methodology, configured as per `frontend.md`. Global styles will be kept to a minimum in `frontend/app/globals.css`.
*   **Interactivity:** Client-side interactivity will be handled using React state and hooks. Server Components will be favored where possible for performance, with Client Components (`'use client'`) used for interactive sections.

## 6. Technical Considerations

### 6.1. Backend
*   **Framework:** Python with FastAPI for its performance and ease of development.
*   **Logic:** Will house the core logic for all tools.

### 6.2. Frontend
*   **Framework:** Next.js with React.
*   **Styling:** Tailwind CSS.
*   **Static Content:** Markdown files for documentation and potentially parts of the homepage.

### 6.3. Data Storage
*   **Primary:** SQLite for local data storage (e.g., saved tool outputs, user notes if implemented). To be used with SQLAlchemy and Alembic for migrations. (Decision documented in `docs/adr/ADR-001-database-choice.md`).
*   **Export:** Functionality to export data to CSV.
*   **Google Sheets Support (Optional Feature):**
    *   Provide functionality for optional two-way synchronization (import/export) between the local SQLite database and a user's Google Sheets.
    *   This feature will require user authentication with Google and explicit user action to initiate sync.
    *   The backend will facilitate this interaction, reading/writing from/to the local SQLite DB.

### 6.4. Modularity
*   The backend `tools/` directory should be designed to allow for straightforward addition of new tool modules. Each tool might have its own subdirectory or a set of clearly defined files.

## 7. Future Considerations / Roadmap

*   Implementation of the Resume Tailoring Utility.
*   Expansion of the Company Research Assistant's data sources.
*   User accounts/profiles (if deemed necessary, though this might conflict with the "fully local, no external dependencies" goal unless handled carefully).
*   More advanced data visualization for tool outputs.
*   Ability to save and manage job applications.

## 8. Out of Scope (for initial MVP)

*   User authentication or cloud-based accounts.
*   Direct integration with job boards (scraping or APIs).
*   Collaborative features.
*   Mobile-first design (desktop-first, responsive is fine).
