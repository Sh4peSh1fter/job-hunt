import json
import csv # Keep for now? Maybe remove later
import os
import logging
import requests
from bs4 import BeautifulSoup
import time
import ollama
import argparse

# Google Sheets Imports
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Google Sheets Configuration ---
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] # Read/write access
# Define columns for the output sheet ("companies-discovery")
COL_COMPANY_NAME = 'A'
COL_COMPANY_DESC_OUTPUT = 'B'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

# --- Copied from sheet_processor.py --- START
def authenticate_google_sheets(credentials_path, token_path):
    """Handles Google Sheets API authentication using OAuth 2.0."""
    creds = None
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            logging.warning(f"Could not load token from {token_path}: {e}. Will re-authenticate.")
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logging.info("Refreshing expired credentials...")
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Could not refresh token: {e}. Need to re-authenticate.")
                creds = None
        else:
            if not os.path.exists(credentials_path):
                logging.error(f"Credentials file not found at: {credentials_path}")
                logging.error("Please download 'credentials.json' from Google Cloud Console.")
                return None
            try:
                logging.info("Starting authentication flow... Your browser might open.")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
                logging.info("Authentication successful.")
            except Exception as e:
                logging.error(f"Authentication failed: {e}")
                return None
        try:
            with open(token_path, 'w') as token_file:
                token_file.write(creds.to_json())
            logging.info(f"Credentials saved to {token_path}")
        except Exception as e:
            logging.error(f"Could not save token to {token_path}: {e}")
    try:
        service = build("sheets", "v4", credentials=creds)
        logging.info("Google Sheets service built successfully.")
        return service
    except Exception as e:
        logging.error(f"Failed to build Google Sheets service: {e}")
        return None
# --- Copied from sheet_processor.py --- END

def load_json(filepath):
    # ... (keep existing function) ...
    """Loads JSON data from a file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        logging.error(f"Error: File not found at {filepath}")
        return None
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from {filepath}: {e}")
        return None
    except Exception as e:
        logging.error(f"Error loading JSON from {filepath}: {e}")
        return None

def load_existing_companies_from_sheet(service, spreadsheet_id, sheet_name):
    """Loads existing company names from Column A of the specified sheet."""
    companies = set()
    try:
        # Read range assumes names are in Column A, starting from row 1 (or 2 if header)
        # Adjust START_ROW if there's a header in the discovery sheet
        DISCOVERY_START_ROW = 1
        read_range = f"{sheet_name}!{COL_COMPANY_NAME}{DISCOVERY_START_ROW}:{COL_COMPANY_NAME}"
        logging.info(f"Reading existing companies from {spreadsheet_id} range {read_range}...")
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=read_range).execute()
        values = result.get('values', [])

        if values:
            for row in values:
                if row: # Check if row is not empty
                    companies.add(row[0].strip())
            logging.info(f"Loaded {len(companies)} existing companies from sheet '{sheet_name}'.")
        else:
            logging.info(f"No existing companies found in sheet '{sheet_name}'.")

    except HttpError as err:
        logging.error(f"API error reading existing companies from sheet: {err}")
        # Decide if script should continue or stop if sheet is inaccessible
    except Exception as e:
        logging.error(f"Unexpected error reading existing companies: {e}")
    return companies

# --- Remove save_companies_to_csv function ---

def append_new_companies_to_sheet(service, spreadsheet_id, sheet_name, new_companies_data):
    """Appends new company names and descriptions to the specified sheet."""
    if not new_companies_data:
        logging.info("No new companies to append to the sheet.")
        return

    values_to_append = []
    for company_info in new_companies_data:
        # Ensure data is in the correct order [Name, Description]
        values_to_append.append([
            company_info.get('name', 'N/A'),
            company_info.get('description', '')
        ])

    body = {
        'values': values_to_append
    }
    try:
        range_to_append = f"{sheet_name}!{COL_COMPANY_NAME}1"
        logging.info(f"Appending {len(values_to_append)} new companies to sheet '{sheet_name}'...")
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_to_append, # Append after the last row with data in Col A
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS", # Inserts rows for the new data
            body=body).execute()
        logging.info(f"{result.get('updates').get('updatedCells')} cells appended.")
    except HttpError as err:
        logging.error(f"API error appending data to sheet: {err}")
    except Exception as e:
        logging.error(f"Unexpected error appending data: {e}")

def extract_company_name_with_llm(context_text, model_name):
    # ... (keep existing function, returns name or None) ...
    """Uses LLM to extract the most likely company/startup name from context text."""
    prompt = f"""Analyze the following text snippet, which is likely a headline or short article summary about a company.
Identify the primary company or startup name being discussed.

**CRITICAL: Respond ONLY with the single, most likely company name.**

*   Do NOT include any introduction, explanation, or surrounding text.
*   If no company name is clearly identifiable, respond with "N/A".
*   Focus on the main subject entity.

Example Input: "Coho AI shuts down, Yotpo to integrate employees amid quiet exit"
Example Output: Coho AI

Example Input: "Intel revives its iconic brand as it fights for relevance"
Example Output: Intel

Example Input: "Investment round completed for Project X"
Example Output: N/A

Text Snippet:
---
{context_text}
---

Company Name:"""

    try:
        logging.debug(f"Sending context to Ollama model {model_name} for company name extraction.")
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.0} # Very low temp for deterministic extraction
        )
        extracted_name = response['message']['content'].strip()

        if extracted_name.lower() == "n/a" or len(extracted_name) > 100: # Avoid long erroneous extractions
            logging.debug(f"  -> LLM indicated no clear company name or result too long ('{extracted_name}').")
            return None

        logging.debug(f"  -> LLM extracted company name: {extracted_name}")
        return extracted_name

    except Exception as e:
        logging.error(f"Error interacting with Ollama model {model_name} for name extraction: {e}")
        return None

def generate_description_with_llm(company_name, context_text, model_name):
    """Generates a brief description of the company based on context."""
    if not company_name or not context_text:
        return ""

    prompt = f"""Based *only* on the text snippet provided below, write a brief, 1-sentence description of the company: '{company_name}'.
Focus on what the company does or its main activity mentioned in the text.

If the text doesn't provide enough information to describe the company, respond with "N/A".
Do not include introductions like "The company...". Just the description sentence or "N/A".

Text Snippet:
---
{context_text}
---

Description:"""

    try:
        logging.debug(f"Sending context to Ollama model {model_name} for description generation.")
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.5} # Slightly higher temp for creative generation
        )
        description = response['message']['content'].strip()

        if description.lower() == "n/a":
            logging.debug(f"  -> LLM could not generate description for {company_name}.")
            return ""

        # Optional: Add further cleanup if needed
        logging.debug(f"  -> LLM generated description: {description}")
        return description

    except Exception as e:
        logging.error(f"Error interacting with Ollama model {model_name} for description generation: {e}")
        return ""

def scrape_source(source_config, model_name):
    """Scrapes a single source, extracts name+description, returns list of dicts."""
    name = source_config.get('name', 'Unknown Source')
    url = source_config.get('url')
    selector = source_config.get('selector')

    if not url or not selector:
        logging.warning(f"Skipping source '{name}': Missing 'url' or 'selector'.")
        return [] # Return list

    logging.info(f"Scraping source: {name} ({url}) using selector: '{selector}'")
    found_companies_data = [] # List to store {'name': ..., 'description': ...}
    processed_texts = set()
    headers = {'User-Agent': USER_AGENT}

    try:
        response = requests.get(url, headers=headers, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml')
        elements = soup.select(selector)

        if not elements:
            logging.warning(f"No elements found for selector '{selector}' at {url}.")
            return found_companies_data

        for element in elements:
            context_text = element.get_text(strip=True)
            if context_text and context_text not in processed_texts:
                processed_texts.add(context_text)
                use_llm_for_name = "LLM" in source_config.get("notes", "")
                company_name = None

                if use_llm_for_name:
                    logging.debug(f"  -> Using LLM to extract name from: '{context_text[:100]}...'")
                    company_name = extract_company_name_with_llm(context_text, model_name)
                else:
                    company_name = context_text.strip()

                if company_name:
                    # Attempt to generate description
                    description = generate_description_with_llm(company_name, context_text, model_name)
                    found_companies_data.append({
                        "name": company_name,
                        "description": description
                    })

        logging.info(f"  -> Found {len(found_companies_data)} potential company entries from {name}.")
        return found_companies_data

    # ... (keep error handling) ...
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []
    except Exception as e:
        logging.error(f"Error scraping {name}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Scrape company names and descriptions from web sources and append to Google Sheet.')
    # --- Updated Arguments ---
    parser.add_argument('-s', '--spreadsheet-id', required=True,
                        help='The ID of the Google Sheet (from its URL).')
    parser.add_argument('-n', '--sheet-name', default='companies-discovery',
                        help='The sheet name within the spreadsheet to write discovered companies.')
    parser.add_argument('--sources', default='sources.json',
                        help='Path to the JSON file containing source URLs and selectors.')
    parser.add_argument('--delay', type=float, default=1.0,
                         help='Delay in seconds between scraping sources.')
    parser.add_argument('-m', '--model', default='llama3:8b',
                        help='Name of the local Ollama model to use.')
    parser.add_argument('--creds', default='credentials.json',
                        help='Path to the Google API credentials JSON file.')
    parser.add_argument('--token', default='token.json',
                        help='Path to store/load the Google API token JSON file.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging.')
    # --- Removed output argument ---

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Construct full paths for credentials/token/sources relative to script location
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir) # Go up one level to 'tools'

    creds_path = args.creds
    if not os.path.isabs(creds_path):
        # Default path is now relative to parent_dir (tools/)
        creds_path = os.path.join(parent_dir, os.path.basename(creds_path))
    token_path = args.token
    if not os.path.isabs(token_path):
        # Default path is now relative to parent_dir (tools/)
        token_path = os.path.join(parent_dir, os.path.basename(token_path))
    sources_path = args.sources
    if not os.path.isabs(sources_path):
        # sources.json stays relative to script dir
        sources_path = os.path.join(script_dir, sources_path)

    # Authenticate Google Sheets
    logging.info("Authenticating with Google Sheets API...")
    sheets_service = authenticate_google_sheets(creds_path, token_path)
    if not sheets_service:
        logging.error("Sheet authentication failed. Exiting.")
        return

    # Load Sources Config
    sources_config = load_json(sources_path)
    if not sources_config or not isinstance(sources_config, list):
        logging.error("Failed to load sources configuration. Exiting.")
        return

    # Check Ollama connection if needed
    model_name = args.model
    requires_llm = any("LLM" in source.get("notes", "") for source in sources_config)
    if requires_llm:
        try:
            ollama.list()
            logging.info(f"Ollama connection successful. Using model: {model_name}")
        except Exception as e:
            logging.error(f"Ollama connection failed: {e}. Exiting.")
            return

    # Load existing companies from the target sheet
    spreadsheet_id = args.spreadsheet_id
    sheet_name = args.sheet_name
    existing_companies_set = load_existing_companies_from_sheet(sheets_service, spreadsheet_id, sheet_name)

    new_companies_to_append = [] # List to store {'name': ..., 'description': ...}

    for source in sources_config:
        scraped_companies_data = scrape_source(source, model_name)

        # Filter out companies already in the sheet
        for company_data in scraped_companies_data:
            if company_data['name'] not in existing_companies_set:
                new_companies_to_append.append(company_data)
                existing_companies_set.add(company_data['name']) # Add to set to avoid duplicates within this run

        logging.info(f"Found {len(new_companies_to_append)} new unique companies so far.")
        time.sleep(args.delay)

    # Append all newly found unique companies to the sheet
    if new_companies_to_append:
        append_new_companies_to_sheet(sheets_service, spreadsheet_id, sheet_name, new_companies_to_append)
    else:
        logging.info("No new companies were discovered in this run.")

    logging.info("Company discovery finished.")

if __name__ == "__main__":
    main() 