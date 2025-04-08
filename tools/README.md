# Job Hunt Automation Tools

This directory contains various Python scripts designed to assist and automate parts of the job hunting process.

## Overview

These tools leverage local AI models (via Ollama) and interact with Google Sheets for data storage and processing.

**Key Technologies:**

*   Python
*   Poetry (for dependency management)
*   Ollama (for running local LLMs like Llama 3, Mistral)
*   Google Sheets API
*   Beautiful Soup & Requests (for web scraping)
*   Matplotlib & Plotly (for data visualization)

## General Setup

1.  **Python:** Ensure you have Python 3.11+ installed.
2.  **Poetry:** Install Poetry ([https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation)).
3.  **Dependencies:** Navigate to this `tools/` directory in your terminal and install all project dependencies:
    ```bash
    cd path/to/job-hunt/tools
    # Activate venv first if you installed Poetry within the venv
    # source .venv/bin/activate
    poetry install --no-root
    # deactivate # if you activated
    ```
4.  **Ollama:** Install and run Ollama ([https://ollama.com/](https://ollama.com/)). Pull desired models (e.g., `ollama pull llama3:8b`).
5.  **Google Cloud Setup:**
    *   Create a Google Cloud Project.
    *   Enable the **Google Sheets API**.
    *   Create **OAuth 2.0 Credentials** for a **Desktop app**.
    *   Download the credentials file, rename it to `credentials.json`, and place it **directly in this `tools/` directory**.
    *   Add your Google account email as a **Test user** on the OAuth consent screen.
6.  **.gitignore:** Ensure the root `.gitignore` file includes `tools/credentials.json` and `tools/token.json`.

## Available Tools

*   **`get-job-keywords/`**: Processes a job application tracking sheet (Google Sheet). Uses an LLM to extract keywords, job details, company info, etc., from job descriptions and populates empty cells. Also generates summary plots.
    *   See `get-job-keywords/README.md` for detailed usage.
*   **`get-companies/`**: Scrapes configured web sources to discover potential companies. Uses an LLM to extract names (if needed) and generate brief descriptions. Appends unique findings to a specified Google Sheet.
    *   See `get-companies/README.md` for detailed usage.

## Running Tools

Always run the scripts from the **project root directory** (`job-hunt/`) using `python`, ensuring the Poetry virtual environment is active if necessary.

**Example (Sheet Processor):**
```bash
source tools/.venv/bin/activate # If needed
python tools/get-job-keywords/sheet_processor.py -s YOUR_SPREADSHEET_ID
deactivate # If needed
```

**Example (Company Discovery):**
```bash
source tools/.venv/bin/activate # If needed
python tools/get-companies/get_companies.py -s YOUR_SPREADSHEET_ID
deactivate # If needed
```

Refer to the specific README file within each tool's directory for detailed arguments and configuration. 