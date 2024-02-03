import time
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

# Authentication setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']  # Includes both read and write permissions
SERVICE_ACCOUNT_FILE = 'credentials.json'  # Replace with your credentials file path

creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# The ID of the spreadsheet to access
SAMPLE_SPREADSHEET_ID = '1eXR4KHzNhaVUC4229_eT0OOaNCnjkA1kEyh3G5Z63wg'  # Replace with your spreadsheet ID

# Function to retrieve all data from the spreadsheet
def get_all_data():
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Get all sheets in the spreadsheet
    sheet_metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    sheets = sheet_metadata.get('sheets', [])

    all_data = []
    for sheet_properties in sheets:
        sheet_title = sheet_properties.get('properties', {}).get('title')

        # Get all values from the current sheet
        result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f'{sheet_title}!A:Z').execute()
        values = result.get('values', [])

        all_data.append({
            'sheet_title': sheet_title,
            'data': values
        })

    return all_data

# Function to write data to the spreadsheet
def write_data(sheet_title, cell_range, new_values):
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    range_to_edit = f'{sheet_title}!{cell_range}'
    body = {
        'values': new_values
    }

    try:
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=range_to_edit, valueInputOption='USER_ENTERED', body=body).execute()
        print(f"{result.get('updatedCells')} cells updated.")
    except HttpError as error:
        print(f"An error occurred: {error}")


data = get_all_data()
data = [row for row in data[0]['data']]
print(type(data))
print(data)

new_data = ['5','Manoj','7894561237','1','','0']
write_data("Sheet1","A6:F6",[new_data])