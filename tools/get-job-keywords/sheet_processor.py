import argparse
import os
import logging
import ollama
from collections import Counter
import time # For potential rate limiting
import json # Added for parsing LLM JSON output
import pandas as pd # Added for Sankey
import plotly.graph_objects as go # Added for Sankey
import matplotlib.pyplot as plt # Added for keyword plot
import matplotlib # Added for backend selection

# Google Sheets Imports
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Ensure matplotlib uses a backend that doesn't require GUI
matplotlib.use('Agg')

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Google Sheets Configuration ---
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"] # Read/write access

# --- Column Configuration (Based on Screenshot - Adjust if needed) ---
# Assumes headers are in row 2. Data starts in row 3.
# Provide the *letter* of the column
COL_COMPANY_SIZE = 'C' # Added
COL_COMPANY_DESC = 'D' # Added
COL_JOB_TITLE = 'G' # Added
COL_JOB_LOCATION = 'H'
COL_JOB_DESC = 'I'
COL_JOB_KEYWORDS = 'J'
HEADER_ROW = 2
START_ROW = 3

# Timeline Columns (Letters)
COL_SCREENING = 'K'
COL_ASSIGNMENT = 'L'
COL_INTERVIEW1 = 'M'
COL_INTERVIEW2 = 'N'
COL_INTERVIEW3 = 'O'
COL_OFFER = 'P'
COL_FEEDBACK = 'Q' # Often indicates rejection if offer column is empty

def authenticate_google_sheets(credentials_path, token_path):
    """Handles Google Sheets API authentication using OAuth 2.0."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_path):
        try:
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        except Exception as e:
            logging.warning(f"Could not load token from {token_path}: {e}. Will re-authenticate.")
            creds = None # Force re-authentication

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                logging.info("Refreshing expired credentials...")
                creds.refresh(Request())
            except Exception as e:
                logging.error(f"Could not refresh token: {e}. Need to re-authenticate.")
                creds = None # Force re-authentication
        else:
            if not os.path.exists(credentials_path):
                logging.error(f"Credentials file not found at: {credentials_path}")
                logging.error("Please download 'credentials.json' from Google Cloud Console and place it there.")
                return None
            try:
                logging.info("Starting authentication flow... Your browser might open.")
                flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
                # Add prompt='consent' to force re-consent if needed for testing scope changes
                # creds = flow.run_local_server(port=0, prompt='consent')
                creds = flow.run_local_server(port=0)
                logging.info("Authentication successful.")
            except Exception as e:
                logging.error(f"Authentication failed: {e}")
                return None
        # Save the credentials for the next run
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

def parse_llm_json_output(response_text):
    """Attempts to parse a JSON object from the LLM response."""
    try:
        # Find the start and end of the JSON block (might be wrapped in ```json ... ```)
        json_start = response_text.find('{')
        json_end = response_text.rfind('}')

        if json_start == -1 or json_end == -1:
            logging.warning(f"Could not find JSON object in LLM output: {response_text}")
            return None

        json_string = response_text[json_start:json_end+1]
        parsed_data = json.loads(json_string)

        # Basic validation for all expected keys
        if not isinstance(parsed_data.get('keywords'), list):
            parsed_data['keywords'] = []
        if not isinstance(parsed_data.get('location'), str):
             parsed_data['location'] = ""
        if not isinstance(parsed_data.get('job_title'), str):
             parsed_data['job_title'] = ""
        if not isinstance(parsed_data.get('company_size'), str):
             parsed_data['company_size'] = ""
        if not isinstance(parsed_data.get('company_description'), str):
             parsed_data['company_description'] = ""

        return parsed_data
    except json.JSONDecodeError as e:
        logging.warning(f"JSONDecodeError parsing LLM output: {e}. Response: {response_text}")
        return None
    except Exception as e:
        logging.warning(f"Error parsing LLM JSON output: {e}. Response: {response_text}")
        return None

def extract_data_with_llm(text, model_name):
    """Extracts structured data from text using a local LLM."""
    # Updated prompt asking for more fields in JSON output
    prompt = f"""Analyze the job description below. Extract the following information:
1.  `keywords`: A list of key technical skills, tools, platforms, methodologies, and important soft skills (as strings).
2.  `location`: The primary work location mentioned (as a single string).
3.  `job_title`: The job title being advertised (as a single string).
4.  `company_size`: Any information indicating the size of the company (e.g., "10-50 employees", "Startup", "Large Corporation") (as a single string).
5.  `company_description`: A brief (1-2 sentence) summary of what the company does, based *only* on the text provided below (as a single string).

**CRITICAL: Respond ONLY with a valid JSON object containing these five keys.**

*   Use appropriate empty values (`[]` for keywords, `""` or `null` for strings) if information cannot be found in the text.
*   Do NOT include any text outside the JSON object (no introductions, explanations, etc.).
*   Ensure the JSON is correctly formatted.

Example Output:
```json
{{
  "keywords": ["Python", "React", "Node.js", "AWS", "SQL", "Problem Solving"],
  "location": "Remote (USA)",
  "job_title": "Senior Software Engineer",
  "company_size": "50-200 employees",
  "company_description": "A fintech company developing tools for financial advisors."
}}
```

Job Description:
---
{text}
---

JSON Output:"""

    try:
        logging.debug(f"Sending request to Ollama model {model_name}")
        response = ollama.chat(
            model=model_name,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.1}
        )
        extracted_data = parse_llm_json_output(response['message']['content'])
        logging.debug(f"LLM ({model_name}) extracted data: {extracted_data}")
        return extracted_data
    except Exception as e:
        logging.error(f"Error interacting with Ollama model {model_name}: {e}")
        logging.error("Ensure Ollama server is running and model '{model_name}' is pulled.")
        return None

def determine_status(row, indices):
    """Determines the final status of an application based on timeline columns."""
    # Check for offer first
    if len(row) > indices['offer'] and row[indices['offer']].strip():
        return "Offer"
    # Check for interviews (any interview column filled)
    if any(len(row) > idx and row[idx].strip() for col, idx in indices.items() if col.startswith('interview')):
        return "Interview Stage (No Offer)"
    # Check for screening/assignment without interview/offer
    if any(len(row) > indices[col] and row[indices[col]].strip() for col in ['screening', 'assignment']):
        return "Rejected (Early Stage)"
    # Check if feedback exists without offer (often means rejected)
    if len(row) > indices['feedback'] and row[indices['feedback']].strip():
        return "Rejected"

    # If none of the above, assume No Answer yet
    return "No Answer"

def plot_keyword_frequency(keyword_counts, output_filename="keywords_frequency.png", top_n=25):
    """Generates and saves a bar chart of the top N keyword frequencies."""
    if not keyword_counts:
        logging.warning("No keyword data to plot.")
        return

    # Get the top N keywords
    top_keywords = keyword_counts.most_common(top_n)
    if not top_keywords:
        logging.warning("No keywords found after filtering.")
        return

    keywords, counts = zip(*top_keywords)

    plt.figure(figsize=(12, max(8, top_n * 0.4))) # Adjust figure size based on N
    plt.barh(range(len(keywords)), counts, align='center')
    plt.yticks(range(len(keywords)), keywords)
    plt.xlabel('Number of Job Descriptions Mentioned')
    plt.title(f'Top {len(keywords)} Most Frequent Keywords')
    plt.gca().invert_yaxis()  # Display the highest count at the top
    plt.tight_layout()

    try:
        plt.savefig(output_filename)
        logging.info(f"Keyword frequency plot saved to {output_filename}")
    except Exception as e:
        logging.error(f"Failed to save keyword plot: {e}")
    plt.close() # Close the plot figure

def plot_status_sankey(statuses, output_filename="application_status_sankey.png"):
    """Generates and saves a Sankey diagram of application statuses."""
    if not statuses:
        logging.warning("No status data to plot.")
        return

    # Define the stages and flow based on the provided screenshot structure
    # This requires interpreting the statuses into logical flows

    labels_dict = {
        "Applications": 0,
        "No Answer": 1,
        "Rejected": 2,        # Combined rejections
        "Interviews": 3,      # Combined interviews
        "Offer": 4,
        "No Offer": 5,        # From Interview stage
        # Add intermediate stages if needed based on more granular status determination
    }
    labels = list(labels_dict.keys())

    source = []
    target = []
    value = []
    color_link = [] # Optional: for coloring links
    color_node = ['blue', 'grey', 'red', 'purple', 'green', 'orange'] # Example node colors

    total_applications = len(statuses)

    # Count transitions (this is simplified based on the screenshot)
    no_answer_count = statuses.count("No Answer")
    rejected_count = statuses.count("Rejected") + statuses.count("Rejected (Early Stage)")
    interviews_count = statuses.count("Interview Stage (No Offer)") + statuses.count("Offer")
    offer_count = statuses.count("Offer")
    no_offer_count = statuses.count("Interview Stage (No Offer)")

    # Flow: Applications -> No Answer
    if no_answer_count > 0:
        source.append(labels_dict["Applications"])
        target.append(labels_dict["No Answer"])
        value.append(no_answer_count)
        color_link.append('rgba(128,128,128,0.6)') # Grey

    # Flow: Applications -> Rejected (without interview)
    if rejected_count > 0:
        source.append(labels_dict["Applications"])
        target.append(labels_dict["Rejected"])
        value.append(rejected_count)
        color_link.append('rgba(255,0,0,0.6)') # Red

    # Flow: Applications -> Interviews (aggregate)
    if interviews_count > 0:
        source.append(labels_dict["Applications"])
        target.append(labels_dict["Interviews"])
        value.append(interviews_count)
        color_link.append('rgba(128,0,128,0.6)') # Purple

    # Flow: Interviews -> Offer
    if offer_count > 0:
        source.append(labels_dict["Interviews"])
        target.append(labels_dict["Offer"])
        value.append(offer_count)
        color_link.append('rgba(0,128,0,0.6)') # Green

    # Flow: Interviews -> No Offer
    if no_offer_count > 0:
        source.append(labels_dict["Interviews"])
        target.append(labels_dict["No Offer"])
        value.append(no_offer_count)
        color_link.append('rgba(255,165,0,0.6)') # Orange

    # Add total application value next to label
    labels[labels_dict["Applications"]] = f"Applications ({total_applications})"

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=labels,
            color=color_node
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=color_link # Apply link colors
        )
    )])

    fig.update_layout(title_text="Job Application Status Flow", font_size=10)

    try:
        # Save static image (requires kaleido or orca, or use psutil)
        fig.write_image(output_filename, engine="auto") # Use auto engine selection
        logging.info(f"Application status Sankey diagram saved to {output_filename}")
    except Exception as e:
        logging.error(f"Failed to save Sankey plot as image: {e}")
        logging.info("Attempting to show plot in browser instead...")
        try:
             fig.show() # Fallback to showing in browser
        except Exception as e_show:
             logging.error(f"Failed to show Sankey plot in browser: {e_show}")

def process_sheet(service, spreadsheet_id, sheet_name, model_name):
    """Reads sheet, processes rows with LLM, updates sheet, then aggregates data for plotting."""
    # --- First Pass: LLM Processing and Sheet Updates ---
    try:
        read_range = f"{sheet_name}!A{START_ROW}:Z"
        logging.info(f"Reading data from {spreadsheet_id} range {read_range} for processing...")
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=read_range).execute()
        values = result.get('values', [])

        if not values:
            logging.info("No data found in the specified range for processing.")
            # Return empty collections if no data to process
            return Counter(), []

        logging.info(f"Found {len(values)} rows of data to potentially process with LLM.")

        updates = []
        col_company_size_index = ord(COL_COMPANY_SIZE.upper()) - ord('A')
        col_company_desc_index = ord(COL_COMPANY_DESC.upper()) - ord('A')
        col_job_title_index = ord(COL_JOB_TITLE.upper()) - ord('A')
        col_location_index = ord(COL_JOB_LOCATION.upper()) - ord('A')
        col_desc_index = ord(COL_JOB_DESC.upper()) - ord('A')
        col_keywords_index = ord(COL_JOB_KEYWORDS.upper()) - ord('A')

        target_columns = {
            COL_JOB_TITLE: {'index': col_job_title_index, 'key': 'job_title', 'type': 'string'},
            COL_JOB_LOCATION: {'index': col_location_index, 'key': 'location', 'type': 'string'},
            COL_JOB_KEYWORDS: {'index': col_keywords_index, 'key': 'keywords', 'type': 'list'},
            COL_COMPANY_SIZE: {'index': col_company_size_index, 'key': 'company_size', 'type': 'string'},
            COL_COMPANY_DESC: {'index': col_company_desc_index, 'key': 'company_description', 'type': 'string'}
        }

        for i, row in enumerate(values):
            current_row_index = START_ROW + i
            job_desc = row[col_desc_index] if len(row) > col_desc_index else ""

            if not job_desc:
                logging.debug(f"Skipping LLM processing for row {current_row_index}: No job description found.")
                continue

            needs_llm_processing = False
            for col_letter, col_info in target_columns.items():
                existing_value = row[col_info['index']] if len(row) > col_info['index'] else ""
                if not existing_value:
                    needs_llm_processing = True
                    break

            if needs_llm_processing:
                logging.info(f"Processing row {current_row_index} with LLM: Found job description and missing data.")
                extracted_data = extract_data_with_llm(job_desc, model_name)
                if extracted_data:
                    logging.info(f"  -> LLM analysis complete for row {current_row_index}.")
                    for col_letter, col_info in target_columns.items():
                        existing_value = row[col_info['index']] if len(row) > col_info['index'] else ""
                        extracted_value = extracted_data.get(col_info['key'])
                        if not existing_value:
                            value_to_write = None
                            if col_info['type'] == 'list' and isinstance(extracted_value, list) and extracted_value:
                                value_to_write = ", ".join(extracted_value)
                            elif col_info['type'] == 'string' and isinstance(extracted_value, str) and extracted_value:
                                value_to_write = extracted_value
                            if value_to_write:
                                logging.info(f"    -> Preparing {col_info['key']} update: {value_to_write[:100]}{'...' if len(value_to_write)>100 else ''}")
                                update_range = f"{sheet_name}!{col_letter}{current_row_index}"
                                updates.append({
                                    'range': update_range,
                                    'values': [[value_to_write]]
                                })
                else:
                    logging.warning(f"  -> Failed to extract or parse data via LLM for row {current_row_index}.")
            else:
                 logging.debug(f"Skipping LLM processing for row {current_row_index}: All target fields already filled.")

        # Perform batch update if there are any changes
        if updates:
            logging.info(f"Applying {len(updates)} updates to the sheet...")
            body = {
                'valueInputOption': 'USER_ENTERED',
                'data': updates
            }
            try:
                update_result = sheet.values().batchUpdate(
                    spreadsheetId=spreadsheet_id, body=body).execute()
                logging.info(f"{update_result.get('totalUpdatedCells')} cells updated.")
                # Optional: Add a small delay to allow updates to propagate before re-reading
                time.sleep(2)
            except HttpError as error:
                logging.error(f"An API error occurred during batch update: {error}")
                # Decide if we should proceed to aggregation despite update error
        else:
            logging.info("No LLM-based updates applied to the sheet.")

    except HttpError as err:
        logging.error(f"An API error occurred during sheet processing: {err}")
        return Counter(), [] # Return empty on critical read/update error
    except Exception as e:
        logging.error(f"An unexpected error occurred during sheet processing: {e}")
        return Counter(), [] # Return empty on other critical errors

    # --- Second Pass: Aggregate Data for Plotting from potentially updated sheet ---
    all_keywords_aggregate = Counter()
    application_statuses = []
    try:
        # Re-read the necessary columns for aggregation (Keywords J, Timeline K-Q)
        # Adjust range to only fetch needed columns for efficiency
        aggregation_range = f"{sheet_name}!{COL_JOB_KEYWORDS}{START_ROW}:{COL_FEEDBACK}"
        logging.info(f"Reading data from {spreadsheet_id} range {aggregation_range} for plotting aggregation...")
        result_agg = sheet.values().get(spreadsheetId=spreadsheet_id, range=aggregation_range).execute()
        values_agg = result_agg.get('values', [])

        if not values_agg:
            logging.warning("No data found in the specified range for aggregation.")
            return all_keywords_aggregate, application_statuses

        logging.info(f"Aggregating plotting data from {len(values_agg)} rows.")

        # Define indices relative to the *aggregation range* (J to Q)
        agg_keywords_index = ord(COL_JOB_KEYWORDS.upper()) - ord(COL_JOB_KEYWORDS.upper()) # Index 0
        agg_timeline_indices = {
            'screening': ord(COL_SCREENING.upper()) - ord(COL_JOB_KEYWORDS.upper()), # K - J = 1
            'assignment': ord(COL_ASSIGNMENT.upper()) - ord(COL_JOB_KEYWORDS.upper()),# L - J = 2
            'interview1': ord(COL_INTERVIEW1.upper()) - ord(COL_JOB_KEYWORDS.upper()),# M - J = 3
            'interview2': ord(COL_INTERVIEW2.upper()) - ord(COL_JOB_KEYWORDS.upper()),# N - J = 4
            'interview3': ord(COL_INTERVIEW3.upper()) - ord(COL_JOB_KEYWORDS.upper()),# O - J = 5
            'offer': ord(COL_OFFER.upper()) - ord(COL_JOB_KEYWORDS.upper()),     # P - J = 6
            'feedback': ord(COL_FEEDBACK.upper()) - ord(COL_JOB_KEYWORDS.upper())  # Q - J = 7
        }

        for row in values_agg:
            # Aggregate Keywords
            existing_keywords_str = row[agg_keywords_index] if len(row) > agg_keywords_index else ""
            if existing_keywords_str:
                try:
                    kw_list = [kw.strip() for kw in existing_keywords_str.split(',') if kw.strip()]
                    all_keywords_aggregate.update(kw_list)
                except Exception as e:
                    logging.warning(f"Could not parse keywords during aggregation: '{existing_keywords_str}' - {e}")

            # Determine Status
            status = determine_status(row, agg_timeline_indices) # Use relative indices
            application_statuses.append(status)

    except HttpError as err:
        logging.error(f"An API error occurred during data aggregation read: {err}")
        # Return whatever might have been collected before error
    except Exception as e:
        logging.error(f"An unexpected error occurred during data aggregation: {e}")

    return all_keywords_aggregate, application_statuses

def main():
    parser = argparse.ArgumentParser(description='Analyze job descriptions from a Google Sheet and update it with keywords using a local LLM.')
    parser.add_argument('-s', '--spreadsheet-id', required=True,
                        help='The ID of the Google Sheet (from its URL).')
    parser.add_argument('-n', '--sheet-name', default='application-track', # Changed default
                        help='The name of the sheet within the spreadsheet to process.')
    parser.add_argument('-m', '--model', default='llama3',
                        help='Name of the local Ollama model to use (e.g., llama3, mistral).')
    parser.add_argument('--creds', default='credentials.json',
                        help='Path to the Google API credentials JSON file.')
    parser.add_argument('--token', default='token.json',
                        help='Path to store/load the Google API token JSON file.')
    parser.add_argument('--keywords-plot', default='keywords_frequency.png',
                        help='Filename for the keyword frequency plot.')
    parser.add_argument('--status-plot', default='application_status_sankey.png',
                        help='Filename for the application status Sankey plot.')
    parser.add_argument('--top-n-keywords', type=int, default=25,
                        help='Number of top keywords to show in the plot.')
    parser.add_argument('--debug', action='store_true',
                        help='Enable debug logging.')

    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    # Construct full paths for credentials/token relative to script's PARENT directory
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

    # Authenticate and build service
    logging.info("Authenticating with Google Sheets API...")
    sheets_service = authenticate_google_sheets(creds_path, token_path)

    if not sheets_service:
        logging.error("Failed to authenticate or build Google Sheets service. Exiting.")
        return

    model_name = args.model
    spreadsheet_id = args.spreadsheet_id
    sheet_name = args.sheet_name

    logging.info(f"Starting processing for Sheet ID: {spreadsheet_id}, Sheet Name: {sheet_name} using model: {model_name}")
    # Get aggregated data from processing
    keyword_data, status_data = process_sheet(sheets_service, spreadsheet_id, sheet_name, model_name)
    logging.info("Sheet processing finished.")

    # Generate plots if data exists
    if keyword_data:
        logging.info("Generating keyword frequency plot...")
        plot_keyword_frequency(keyword_data, args.keywords_plot, args.top_n_keywords)
    else:
        logging.warning("Skipping keyword plot generation: No keyword data collected.")

    if status_data:
        logging.info("Generating application status Sankey plot...")
        plot_status_sankey(status_data, args.status_plot)
    else:
        logging.warning("Skipping status plot generation: No status data collected.")

    logging.info("Script finished.")

if __name__ == "__main__":
    main()
