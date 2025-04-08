# Job Application Sheet Processor Tool

This tool interacts with a Google Sheet ("application-track") used for tracking job applications. It uses a local Large Language Model (LLM) via Ollama to automatically populate empty fields (like Job Title, Location, Keywords, Company Size, Company Description) based on the Job Description column. It also generates summary plots for keyword frequency and application status.

## Purpose

To automate the enrichment of a job application tracking spreadsheet by:

*   Extracting key information from job descriptions using an LLM.
*   Populating relevant columns in the spreadsheet automatically.
*   Providing visual summaries of keyword trends and application pipeline status.

## Methodology

1.  **Authentication:** Authenticates with the Google Sheets API using OAuth 2.0 (requires `credentials.json` setup, creates/uses `token.json`). Shared credentials should be placed in the parent `tools/` directory.
2.  **Read Sheet Data:** Reads application data from the specified sheet (default: "application-track") within the provided Google Spreadsheet ID.
3.  **Identify Rows for Processing:** Identifies rows that have a job description (Column I) but are missing data in one or more target fields (Company Size, Company Desc, Job Title, Location, Keywords).
4.  **LLM Enrichment:** For each row identified:
    *   Sends the job description text to the configured local Ollama LLM.
    *   Prompts the LLM to return a JSON object containing extracted values for `job_title`, `location`, `keywords`, `company_size`, and `company_description`.
    *   Parses the LLM's JSON response.
5.  **Sheet Update:** Prepares and sends a batch update request to Google Sheets, populating *only* the cells that were originally empty *and* for which the LLM successfully provided data.
6.  **Data Aggregation for Plots:** After the updates, re-reads the relevant columns (Keywords and Timeline columns) from the sheet.
7.  **Keyword Aggregation:** Parses the comma-separated keywords from the keyword column (Column J) across all rows and aggregates their total frequency.
8.  **Status Determination:** Analyzes the timeline columns (K-Q) for each row to determine its final status (e.g., "No Answer", "Rejected", "Interview Stage (No Offer)", "Offer").
9.  **Plot Generation:**
    *   Creates a horizontal bar chart (`keywords_frequency.png`) showing the frequency of the most common keywords using Matplotlib.
    *   Creates a Sankey diagram (`application_status_sankey.png`) visualizing the application status flow using Plotly. Attempts to save as PNG, falling back to opening in a browser if PNG saving fails (due to potential issues with static image export dependencies like Kaleido).

## Setup Requirements

1.  **Python:** Version 3.11 or higher (as specified in `tools/pyproject.toml`).
2.  **Ollama:** You need Ollama installed and running locally with a suitable model pulled (e.g., `ollama pull llama3:8b`).
3.  **Google Cloud Project:**
    *   Enable the **Google Sheets API**.
    *   Create **OAuth 2.0 Credentials** for a **Desktop app**.
    *   Download the credentials JSON file, rename it to `credentials.json`, and place it in the **parent `tools/` directory**.
    *   Add your Google account email as a **Test user** in the OAuth consent screen settings (while the app is in "Testing" status).
4.  **Python Dependencies:** Navigate to the `tools/` directory and ensure dependencies are installed using Poetry:
    ```bash
    cd tools
    # If you haven't installed dependencies for other tools yet:
    # source .venv/bin/activate # If using venv-in-project
    # poetry install --no-root
    # deactivate # If using venv-in-project
    ```
    This ensures `ollama`, Google API client libraries, `matplotlib`, `pandas`, `plotly`, and `psutil` are installed.
5.  **Google Sheet:** The target spreadsheet must exist and contain a sheet with the expected name (default: "application-track") and columns (C: Company Size, D: Company Desc, G: Job Title, H: Location, I: Job Description, J: Keywords, K-Q: Timeline/Status columns).
6.  **.gitignore:** Ensure `tools/credentials.json` and `tools/token.json` are included in your project's `.gitignore` file.

## Usage

Run the script from the project root, ensuring Poetry's environment is active if needed.

```bash
# Activate venv if needed (adjust path if not in project root)
source tools/.venv/bin/activate

# Run the script (replace with your Spreadsheet ID)
python tools/get-job-keywords/sheet_processor.py -s YOUR_SPREADSHEET_ID_HERE [options]

# Deactivate venv if needed
deactivate
```

**Required Argument:**

*   `-s`, `--spreadsheet-id SPREADSHEET_ID`: The ID of the Google Sheet (from its URL) containing the "application-track" data.

**Optional Arguments:**

*   `-n`, `--sheet-name SHEET_NAME`: Name of the sheet within the spreadsheet to process (default: `application-track`).
*   `-m`, `--model MODEL_NAME`: Name of the local Ollama model to use (default: `llama3:8b`).
*   `--creds FILE_PATH`: Path to the Google API `credentials.json` file (default: `../credentials.json` relative to script, i.e., in `tools/`).
*   `--token FILE_PATH`: Path to store/load the Google API `token.json` file (default: `../token.json` relative to script, i.e., in `tools/`).
*   `--keywords-plot FILE_PATH`: Filename for the keyword frequency plot (default: `keywords_frequency.png` in the current run directory).
*   `--status-plot FILE_PATH`: Filename for the application status Sankey plot (default: `application_status_sankey.png` in the current run directory).
*   `--top-n-keywords N`: Number of top keywords to show in the plot (default: `25`).
*   `--debug`: Enable more detailed logging output.

**Example:**

```bash
# Run with defaults for sheet "application-track"
python tools/get-job-keywords/sheet_processor.py -s abc123spreadsheetIdxyz

# Specify a different sheet name and Ollama model
python tools/get-job-keywords/sheet_processor.py -s abc123spreadsheetIdxyz -n ArchivedApplications -m mistral
```

## Input Format (Google Sheet)

The script expects a sheet (default: "application-track") with headers likely in row 2 and data starting row 3, containing at least these columns:

*   `C`: Company Size
*   `D`: Company Description (About)
*   `G`: Job Title
*   `H`: Job Location
*   `I`: Job Description
*   `J`: Job Keywords
*   `K`-`Q`: Timeline columns used for status determination (Screening, Assignment, Interviews, Offer, Feedback).

The script reads column `I` and attempts to fill empty cells in columns `C`, `D`, `G`, `H`, and `J`.

## Output Format

1.  **Google Sheet Updates:** The script modifies the target Google Sheet directly by filling in empty cells in columns C, D, G, H, and J based on LLM extraction from column I.
2.  **Plot Files:** Generates two image files in the directory where the script is run:
    *   `keywords_frequency.png` (or custom name): Bar chart of top keyword frequencies.
    *   `application_status_sankey.png` (or custom name): Sankey diagram of application statuses. (Note: Saving may fail; script will attempt to open in browser as fallback).

## Limitations and Considerations

*   **LLM Accuracy & Consistency:** The quality of extracted data depends heavily on the LLM, prompt, and job description text. May require prompt tuning. Results can vary.
*   **Processing Time:** LLM processing for each row can be time-consuming.
*   **Resource Usage:** Running the LLM requires significant local RAM/CPU.
*   **Google API Quotas:** Heavy usage might eventually hit Google Sheets API limits (unlikely for typical personal use).
*   **Status Logic:** The `determine_status` function uses simple logic based on which timeline columns are filled. This might need adjustment based on how you use the sheet.
*   **Plotting:** Saving the Sankey diagram requires specific dependencies (`kaleido` or `orca`) which can be difficult to install. The browser fallback should generally work.
*   **Error Handling:** Basic error handling is included, but complex API or LLM issues might require manual debugging.
