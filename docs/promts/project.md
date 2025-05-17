The project is called "job-hunt", and its a local web application designed to assist individuals in managing and optimizing their job search process. It consolidates several focused tools into a single, easy-to-use interface to help streamline common tasks such as analyzing job descriptions, gathering company information, and managing personal search data.
The job search process often involves a wide range of repetitive and fragmented tasks, including tailoring resumes, tracking applications, researching companies, and identifying job-specific keywords. This project aims to bring structure and automation to those efforts by providing a centralized platform that runs locally and does not require any external dependencies or data storage.

The project goals can be listed as follows:
- Centralize useful utilities to support various stages of the job search process
- Automate time-consuming and repetitive tasks
- Maintain user privacy by ensuring all functionality is local and self-hosted
- Provide a modular, extensible architecture to support additional tools in the future
- Deliver a simple and effective user experience

The application includes the following features:
- **Homepage** with static documentation and guidance on how to use the platform effectively
- **Tools section** offering a growing set of utilities (note that the tools should be very easy to manage and add), including:
  - **Keyword Frequency Analyzer**: Extract and count key terms from job descriptions
  - **Company Research Assistant**: Automate information gathering about potential employers
  - **Resume Tailoring Utility** *(planned)*: Match resume content to job descriptions to increase application relevance
- FastAPI-based backend for performance and ease of extension
- Frontend based on the Tailwind Next.js Starter Blog for clear layout and responsive design. An example of it @https://timlrx.github.io/tailwind-nextjs-starter-blog/ (the code located here @https://github.com/timlrx/tailwind-nextjs-starter-blog)
- Clean directory structure for maintainability
- SQLite for local storage and CSV export of tool outputs, and support of google sheets

Technology stack:
- **Backend**: Python, FastAPI
- **Frontend**: Next.js, Tailwind CSS
- **Storage**: SQLite(?)
- **Static Content**: Markdown files

The folder structure should look like this:
```
job-hunt/
├── backend/           # FastAPI application and tools logic
│   ├── main.py
│   └── tools/
├── frontend/          # Next.js frontend application
├── docs/              # Static markdown documentation
├── .cursor/           # Development rules and configurations
└── README.md
```