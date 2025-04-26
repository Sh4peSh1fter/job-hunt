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
# Define the range to read existing data (adjust if needed, e.g., A2:B if headers)
EXISTING_DATA_READ_RANGE = f"{COL_COMPANY_NAME}1:{COL_COMPANY_DESC_OUTPUT}"

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
                # If refresh fails, try full auth flow
                if os.path.exists(token_path):
                    os.remove(token_path) # Remove invalid token
                creds = None # Ensure we proceed to full auth
            # Save the potentially refreshed credentials
            if creds and creds.valid:
                 try:
                    with open(token_path, 'w') as token_file:
                        token_file.write(creds.to_json())
                    logging.info(f"Refreshed credentials saved to {token_path}")
                 except Exception as e:
                    logging.error(f"Could not save refreshed token to {token_path}: {e}")
        else:
            if not os.path.exists(credentials_path):
                logging.error(f"Credentials file not found at: {credentials_path}")
                logging.error("Please download 'credentials.json' from Google Cloud Console.")
                return None
            try:
                logging.info("Starting authentication flow... Your browser might open.")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                # Try specific port first, then random if busy
                try:
                    creds = flow.run_local_server(port=8080) # Common redirect port
                except OSError: # Port might be in use
                     logging.warning("Port 8080 in use, trying random port...")
                     creds = flow.run_local_server(port=0)
                logging.info("Authentication successful.")
            except Exception as e:
                logging.error(f"Authentication failed: {e}")
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
    """
    Loads existing company data (name, description, row) from the specified sheet.
    Returns a dictionary mapping company names to {'row': int, 'description': str}.
    """
    companies_map = {}
    try:
        read_range = f"{sheet_name}!{EXISTING_DATA_READ_RANGE}"
        logging.info(f"Reading existing companies and descriptions from {spreadsheet_id} range {read_range}...")
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=read_range).execute()
        values = result.get('values', [])

        if values:
            # Start row index from 1 (as used in A1 notation)
            start_row_index = int(EXISTING_DATA_READ_RANGE.split(':')[0][len(COL_COMPANY_NAME):])

            for i, row in enumerate(values):
                current_row_index = start_row_index + i
                if row: # Check if row is not empty
                    company_name = row[0].strip() if len(row) > 0 else None
                    description = row[1].strip() if len(row) > 1 else "" # Get description or default to empty
                    if company_name: # Only add if there's a company name
                        companies_map[company_name] = {'row': current_row_index, 'description': description}
            logging.info(f"Loaded {len(companies_map)} existing companies from sheet '{sheet_name}'.")
        else:
            logging.info(f"No existing companies found in sheet '{sheet_name}'.")

    except HttpError as err:
        logging.error(f"API error reading existing companies from sheet: {err}")
    except Exception as e:
        logging.error(f"Unexpected error reading existing companies: {e}")
    return companies_map

# --- Remove save_companies_to_csv function ---

def append_new_companies_to_sheet(service, spreadsheet_id, sheet_name, new_companies_data):
    """Appends new company names and descriptions to the specified sheet."""
    if not new_companies_data:
        logging.info("No new companies to append to the sheet.")
        return 0 # Return count of appended companies

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
    appended_count = 0
    try:
        # Append after the last row with data in the *first column*
        range_to_append = f"{sheet_name}!{COL_COMPANY_NAME}1"
        # --- Added Debug Logging --- START - REMOVE this block? Redundant now.
        # logging.debug(f"Attempting to append {len(values_to_append)} rows.")
        # if values_to_append:
        #     logging.debug(f"First row data to append: {values_to_append[0]}")
        #     if len(values_to_append) > 1:
        #         logging.debug(f"Second row data to append: {values_to_append[1]}")
        # --- Added Debug Logging --- END
        logging.info(f"Appending {len(values_to_append)} new companies to sheet '{sheet_name}'...")
        result = service.spreadsheets().values().append(
            spreadsheetId=spreadsheet_id,
            range=range_to_append, # Append after the last row with data in Col A
            valueInputOption="USER_ENTERED",
            insertDataOption="INSERT_ROWS", # Inserts rows for the new data
            body=body).execute()
        # Get number of cells updated (should be rows * 2)
        updated_cells = result.get('updates', {}).get('updatedCells', 0)
        appended_count = updated_cells // 2 if updated_cells else len(values_to_append) # Estimate if API doesn't return cells reliably
        logging.info(f"{updated_cells} cells appended ({appended_count} companies).")

    except HttpError as err:
        logging.error(f"API error appending data to sheet: {err}")
    except Exception as e:
        logging.error(f"Unexpected error appending data: {e}")
    return appended_count # Return the number of companies appended

def update_company_descriptions_in_sheet(service, spreadsheet_id, sheet_name, updates_to_perform):
    """
    Updates descriptions for existing companies using batchUpdate.
    updates_to_perform: List of dictionaries [{'row': int, 'description': str}]
    """
    if not updates_to_perform:
        logging.info("No company descriptions need updating in the sheet.")
        return 0 # Return count of updated companies

    data = []
    for update in updates_to_perform:
        row_index = update['row']
        description = update['description']
        # Construct the range for the description cell in A1 notation
        target_range = f"{sheet_name}!{COL_COMPANY_DESC_OUTPUT}{row_index}"
        data.append({
            'range': target_range,
            'values': [[description]] # Value needs to be nested list for API
        })

    body = {
        'valueInputOption': 'USER_ENTERED',
        'data': data
    }
    updated_count = 0
    try:
        logging.info(f"Updating descriptions for {len(updates_to_perform)} companies in sheet '{sheet_name}'...")
        result = service.spreadsheets().values().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=body).execute()
        updated_count = result.get('totalUpdatedCells', len(updates_to_perform)) # Use totalUpdatedCells or estimate
        logging.info(f"{updated_count} description cells updated.")
    except HttpError as err:
        logging.error(f"API error batch updating descriptions: {err}")
    except Exception as e:
        logging.error(f"Unexpected error batch updating descriptions: {e}")
    return updated_count # Return the number of companies updated

def extract_company_name_with_llm(context_text, model_name):
    """Uses LLM to extract the most likely company/startup name from context text."""
    prompt = f"""Analyze the following text snippet, which is likely a headline or short article summary about a company.
Identify the primary company or startup name being discussed.

**CRITICAL: Respond ONLY with the single, most likely company name.**

*   Do NOT include any introduction, explanation, or surrounding text.
*   If no company name is clearly identifiable, respond with "N/A".
*   Focus on the main subject entity. Avoid generic terms unless they are part of the name.

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

        # Basic validation
        if not extracted_name or extracted_name.lower() == "n/a" or len(extracted_name) > 100: # Avoid long erroneous extractions
            logging.debug(f"  -> LLM indicated no clear company name or result invalid ('{extracted_name}').")
            return None
        if any(kw in extracted_name.lower() for kw in ["company name:", "description:", "snippet:", "example output:", "example input:"]):
             logging.debug(f"  -> LLM response contained keywords, likely not a valid name ('{extracted_name}').")
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
Do not include introductions like "The company..." or "Description:". Just the description sentence or "N/A".

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

        # Basic cleanup and validation
        if not description or description.lower() == "n/a" or len(description) < 5: # Ignore very short/non-answers
            logging.debug(f"  -> LLM could not generate valid description for {company_name}.")
            return ""
        if description.startswith(("Description:", "The company", "Based on the text")):
            logging.debug(f"  -> LLM description started with preamble, cleaning up: '{description}'")
            # Attempt to remove common preambles
            description = description.split(":", 1)[-1].strip()
            if description.lower().startswith("the company"):
                description = description[len("the company"):].strip()

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
        response = requests.get(url, headers=headers, timeout=30) # Increased timeout
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'lxml') # Use lxml for speed
        elements = soup.select(selector)

        if not elements:
            logging.warning(f"No elements found for selector '{selector}' at {url}.")
            return found_companies_data

        logging.info(f"  -> Found {len(elements)} potential elements matching selector.")
        for i, element in enumerate(elements):
            # Use stripped_strings for potentially cleaner text extraction
            context_parts = list(element.stripped_strings)
            if not context_parts:
                 logging.debug(f"  -> Element {i+1} had no stripped strings.")
                 continue # Skip empty elements
            context_text = " ".join(context_parts)

            if context_text and context_text not in processed_texts:
                processed_texts.add(context_text)
                use_llm_for_name = "LLM" in source_config.get("notes", "")
                company_name = None

                logging.debug(f"  -> Processing text: '{context_text[:150]}...'")

                if use_llm_for_name:
                    company_name = extract_company_name_with_llm(context_text, model_name)
                else:
                    # Use the first line or whole text if simple element?
                    # Keep current logic: assume element text *is* the name if not using LLM
                    company_name = context_text.strip()
                    logging.debug(f"  -> Using element text as company name: {company_name}")

                if company_name:
                    description = generate_description_with_llm(company_name, context_text, model_name)
                    found_companies_data.append({
                        "name": company_name,
                        "description": description
                    })
                else:
                    logging.debug(f"  -> No valid company name extracted/found for text chunk.")

        logging.info(f"  -> Extracted {len(found_companies_data)} name/description pairs from {name}.")
        return found_companies_data

    except requests.exceptions.Timeout:
        logging.error(f"Timeout error fetching {url}")
        return []
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching {url}: {e}")
        return []
    except Exception as e:
        logging.error(f"Error scraping {name}: {e}")
        return []

def main():
    parser = argparse.ArgumentParser(description='Scrape company names and descriptions from web sources, update/append to Google Sheet.')
    # --- Arguments ---
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
    parser.add_argument('--creds', default='../credentials.json', # Adjusted default relative path
                        help='Path to the Google API credentials JSON file.')
    parser.add_argument('--token', default='../token.json', # Adjusted default relative path
                        help='Path to store/load the Google API token JSON file.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging.')
    # --- Removed output argument ---

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("DEBUG logging enabled.")

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
    # Check if *any* source requires LLM for name OR if description generation is implicitly needed
    requires_llm = any("LLM" in source.get("notes", "") for source in sources_config) or True # Assume description always wanted
    if requires_llm:
        try:
            # Add a timeout to the list call
            client = ollama.Client()
            client.list() # Check connection without timeout
            logging.info(f"Ollama connection successful. Using model: {model_name}")
        except Exception as e:
            logging.error(f"Ollama connection failed: {e}. Check if Ollama server is running and model '{model_name}' is pulled. Exiting.")
            return

    # Load existing companies from the target sheet
    spreadsheet_id = args.spreadsheet_id
    sheet_name = args.sheet_name
    existing_companies_map = load_existing_companies_from_sheet(sheets_service, spreadsheet_id, sheet_name)

    # --- Processing Variables ---
    companies_to_append = []      # List of {'name': ..., 'description': ...} for new companies
    descriptions_to_update = []   # List of {'row': ..., 'description': ...} for existing companies
    processed_in_this_run = set() # Track unique company names processed in *this* run to avoid duplicates
    total_potential_companies_found = 0 # Count names extracted/found before uniqueness check

    # --- Scrape Sources ---
    for source in sources_config:
        scraped_data = scrape_source(source, model_name)
        total_potential_companies_found += len(scraped_data)

        for company_data in scraped_data:
            scraped_name = company_data.get('name')
            scraped_description = company_data.get('description', '')

            if not scraped_name: # Skip if no name was extracted
                continue

            # Check if we already processed this exact name in this run
            if scraped_name in processed_in_this_run:
                 logging.debug(f"Skipping duplicate '{scraped_name}' found again in this run.")
                 continue # Already handled (either added to append or update list)

            processed_in_this_run.add(scraped_name)

            # Check against sheet data
            existing_info = existing_companies_map.get(scraped_name)

            if existing_info:
                # Company exists in sheet
                existing_desc = existing_info.get('description', '')
                row_num = existing_info['row']
                # Update if scraped description is valid AND (sheet description is empty OR different)
                if scraped_description and (not existing_desc or scraped_description != existing_desc):
                    logging.info(f"Found updated description for existing company: '{scraped_name}' (Row {row_num}).")
                    descriptions_to_update.append({
                        'row': row_num,
                        'description': scraped_description
                    })
                else:
                     logging.debug(f"Existing company '{scraped_name}' found, description unchanged or no new description found.")
            else:
                # Company is new
                logging.info(f"Found new company: '{scraped_name}'.")
                companies_to_append.append({
                    'name': scraped_name,
                    'description': scraped_description
                })

        logging.info(f"-> Processed source. Total unique companies found so far in run: {len(processed_in_this_run)}")
        logging.info(f"-> Companies queued for append: {len(companies_to_append)}, Updates queued: {len(descriptions_to_update)}")
        time.sleep(args.delay) # Respect delay between sources

    # --- Update and Append to Sheet ---
    updated_count = 0
    appended_count = 0

    if descriptions_to_update:
        updated_count = update_company_descriptions_in_sheet(sheets_service, spreadsheet_id, sheet_name, descriptions_to_update)

    if companies_to_append:
        appended_count = append_new_companies_to_sheet(sheets_service, spreadsheet_id, sheet_name, companies_to_append)

    # --- Final Report ---
    logging.info("--- Company Discovery Finished ---")
    logging.info(f"Total potential company entries found across all sources: {total_potential_companies_found}")
    logging.info(f"Total unique company names processed in this run: {len(processed_in_this_run)}")
    logging.info(f"Number of existing company descriptions updated: {updated_count}")
    logging.info(f"Number of new companies appended to the sheet: {appended_count}")
    logging.info("----------------------------------")

if __name__ == "__main__":
    main() 