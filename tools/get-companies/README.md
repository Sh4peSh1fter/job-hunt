# Company Discovery Tool (`get-companies`)

This tool scrapes specified web sources to discover potential company names for job applications. It uses a local LLM (Ollama) to extract names from context (if needed) and generate brief descriptions based on the scraped text. Discovered unique companies (name and description) are appended as new rows to a specified Google Sheet.

## Purpose

The primary goal is to automate the discovery of companies from various lists or directories online (e.g., startup lists, portfolio pages, industry directories). It aims to provide not just a name, but also a minimal context (a 1-sentence AI-generated description) to aid in the initial filtering process, storing the results directly in your Google Sheets job hunt tracker.

## Methodology

1.  **Configuration:** Reads a list of sources from a JSON file (`sources.json` by default). Each source specifies a URL and a CSS selector to target relevant HTML elements.
2.  **Authentication:** Authenticates with the Google Sheets API using OAuth 2.0 (`credentials.json` and `token.json`). Shared credentials should be placed in the parent `tools/` directory.
3.  **Load Existing:** Reads Column A (Company Names) from the specified target Google Sheet (e.g., "companies-discovery") to identify already discovered companies and avoid duplicates.
4.  **Scraping & Extraction:** For each source defined in the JSON file:
    *   Sends an HTTP GET request to the source URL.
    *   Parses the HTML content.
    *   Extracts text content from elements matching the CSS selector.
    *   **Name Extraction:**
        *   If the source's notes in `sources.json` contain "LLM", it sends the extracted text to the configured Ollama model to identify the primary company name.
        *   Otherwise, it uses the directly extracted text as the name.
    *   **Description Generation:** If a unique company name is identified, it sends the name and the original context text to the Ollama model to generate a brief, 1-sentence description based *only* on that context.
    *   Includes a polite delay between requests to different sources.
5.  **Output:** Appends any newly found, unique company names and their corresponding AI-generated descriptions as new rows to the specified Google Sheet using the Sheets API.

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
    This ensures `requests`, `beautifulsoup4`, `lxml`, `ollama`, and the Google API client libraries are installed.
5.  **.gitignore:** Ensure `tools/credentials.json` and `tools/token.json` are included in your project's `.gitignore` file.

## Configuration (`sources.json`)

This JSON file defines where the script should look for companies. Each object represents a source:

*   `name`: (String) Descriptive name for the source.
*   `url`: (String) The URL to scrape.
*   `selector`: (String) CSS selector targeting HTML element(s) containing the company name or context text.
*   `notes`: (String, Optional) Any comments. **Include the substring "LLM" in the notes if you want the script to use the Ollama model to extract the company name from the text selected by the `selector`** (e.g., if the selector grabs a headline instead of just the name).

**Example `sources.json` entries:**

```json
[
  {
    "name": "Y Combinator Companies",
    "url": "https://www.ycombinator.com/companies",
    "selector": "a._company_86jzd_337 span._companyName_86jzd_411",
    "notes": "Selector targets the specific company name span. Direct extraction."
  },
  {
    "name": "CTech Startups Category",
    "url": "https://www.calcalistech.com/ctechnews/category/5214",
    "selector": "h3.title",
    "notes": "Selector targets headline. Use LLM for name extraction and description."
  }
]
```

## Usage

Run the script from the project root, ensuring Poetry's environment is active if needed.

```bash
# Activate venv if needed (adjust path if not in project root)
source tools/.venv/bin/activate

# Run the script (replace with your Spreadsheet ID)
python tools/get-companies/get_companies.py -s YOUR_SPREADSHEET_ID_HERE [options]

# Deactivate venv if needed
deactivate
```

**Required Argument:**

*   `-s`, `--spreadsheet-id SPREADSHEET_ID`: The ID of the Google Sheet (from its URL) where discovered companies will be appended.

**Optional Arguments:**

*   `-n`, `--sheet-name SHEET_NAME`: Name of the sheet within the spreadsheet to write to (default: `companies-discovery`).
*   `--sources FILE_PATH`: Path to the JSON file containing source configurations (default: `sources.json` located next to the script).
*   `--delay SECONDS`: Wait time in seconds between scraping sources (default: `1.0`).
*   `-m`, `--model MODEL_NAME`: Name of the local Ollama model to use (default: `llama3:8b`).
*   `--creds FILE_PATH`: Path to the Google API `credentials.json` file (default: `../credentials.json` relative to script, i.e., in `tools/`).
*   `--token FILE_PATH`: Path to store/load the Google API `token.json` file (default: `../token.json` relative to script, i.e., in `tools/`).
*   `--debug`: Enable more detailed logging output.

**Example:**

```bash
# Run with defaults, writing to 'companies-discovery' sheet in the specified spreadsheet
python tools/get-companies/get_companies.py -s abc123spreadsheetIdxyz

# Specify a different sheet name and Ollama model
python tools/get-companies/get_companies.py -s abc123spreadsheetIdxyz -n MyDiscoveryList -m mistral
```

## Output Format (Google Sheet)

The script appends new rows to the specified sheet (default: "companies-discovery"). Each row contains:

*   **Column A:** Company Name (extracted directly or via LLM).
*   **Column B:** Company Description (1-sentence generated by LLM based on scraped context).

## Limitations and Considerations

*   **Scraping Fragility & Ethics:** Web scraping can break easily if website structures change. Always check website `robots.txt` and Terms of Service.
*   **CSS Selectors:** Requires careful inspection of target websites.
*   **LLM Accuracy:** The quality of extracted names and generated descriptions depends heavily on the LLM, the prompt, and the quality of the scraped context text. Descriptions are based *only* on the limited scraped text, not external knowledge.
*   **Dynamic Content:** May not work well with JavaScript-heavy sites.
*   **Google API Setup:** Requires initial setup in Google Cloud Console.
*   **Resource Usage:** Running the LLM requires adequate local machine resources (RAM, CPU). 