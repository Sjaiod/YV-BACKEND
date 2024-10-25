import pandas as pd
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils.drive_uploader import authenticate
import datetime
import openpyxl
from googleapiclient.errors import HttpError
from io import BytesIO
from googleapiclient.http import MediaIoBaseUpload

def create_new_volunteer_sheet(event_name):
        
    try:
        # Authenticate with Google Drive and Sheets APIs
        creds = authenticate()
        drive_service = build('drive', 'v3', credentials=creds)
        sheets_service = build('sheets', 'v4', credentials=creds)

        # Create the Google Sheets file with the specified name
        file_metadata = {
            'name': f'{event_name}_Volunteer_Sheet',
            'mimeType': 'application/vnd.google-apps.spreadsheet',
            'parents': ['1IBi1xdLWsfKY99ZsSBgoMeiFC6REvO_E']  # Replace with your folder ID
        }

        sheet_file = drive_service.files().create(body=file_metadata, fields='id').execute()
        sheet_id = sheet_file['id']
        
        # Define headers for the new sheet
        columns = ["Name", "Email", "Phone", "Age", "T-shirt Size", "Registration Date", "Food", "TRX ID"]
        
        # Write headers to the sheet
        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Sheet1!A1',  # Assuming default sheet name is "Sheet1"
            valueInputOption='RAW',
            body={'values': [columns]}
        ).execute()

        # Set file permissions to allow access
        permissions = {
            'type': 'anyone',  # For public access
            'role': 'writer',  # 'writer' for write access
        }
        drive_service.permissions().create(fileId=sheet_id, body=permissions).execute()

        # Return the file ID for further operations
        return sheet_id

    except HttpError as e:
        error_reason = e.error_details if hasattr(e, 'error_details') else str(e)
        print(f"An error occurred: {error_reason}")
        return None



def stop_volunteer_intake():
    # Get the path of the Excel sheet from path.txt
    sheets_dir = os.path.join(os.getcwd(), 'volunteers', 'sheets')
    path_file = os.path.join(sheets_dir, 'path.txt')
    
    if not os.path.exists(path_file):
        return "No active volunteer sheet found."
    
    with open(path_file, 'r') as f:
        file_name = f.read().strip()

    # Full path to the Excel file
    file_path = os.path.join(sheets_dir, file_name)

    # Authenticate with Google Drive
    creds = authenticate()  # Assume authenticate() function exists to get Google credentials
    service = build('drive', 'v3', credentials=creds)
    PARENT_FOLDER_ID = "1IBi1xdLWsfKY99ZsSBgoMeiFC6REvO_E"

    # Metadata for the file to be uploaded
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_metadata = {
        'name': f'Volunteer_Sheet_{current_time}.xlsx',  # You can customize this
        'parents': [PARENT_FOLDER_ID],  # Google Drive folder ID
    }

    # Upload the file to Google Drive
    media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Set file permissions to public
    permission = {
        'type': 'anyone',
        'role': 'writer',
    }
    service.permissions().create(fileId=uploaded_file['id'], body=permission).execute()

    # Generate the public URL for the file
    file_url = f"https://drive.google.com/uc?export=view&id={uploaded_file['id']}"

    return file_url

# Function to append new volunteer data to the existing Excel sheetfrom googleapiclient.discovery import build

def append_to_volunteer_sheet(file_id, data):
    try:
        # Authenticate and set up the Google Sheets API
        creds = authenticate()
        service = build('sheets', 'v4', credentials=creds)
        
        # Reference the Sheets service
        sheet = service.spreadsheets()
        
        # Prepare headers and check if they need to be set
        headers = ["Name", "Email", "Phone", "Age", "T-shirt Size", "Registration Date", "Food", "TRX ID"]
        try:
            # Attempt to read headers to see if they already exist
            sheet.values().get(spreadsheetId=file_id, range='Sheet1!A1:H1').execute()
        except HttpError:
            # If header row does not exist, create it
            sheet.values().update(
                spreadsheetId=file_id,
                range='Sheet1!A1',
                valueInputOption='RAW',
                body={'values': [headers]}
            ).execute()
        
        # Prepare new row data
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_row = [
            data.get('name', ''),
            data.get('email', ''),
            data.get('phone', ''),
            data.get('age', ''),
            data.get('tshirt_size', ''),
            current_time,  # Registration date
            data.get('food', ''),
            data.get('trx_id', '')
        ]
        
        # Append the new row of data
        sheet.values().append(
            spreadsheetId=file_id,
            range='Sheet1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body={'values': [new_row]}
        ).execute()
        
        print("Data appended successfully.")
        return True

    except HttpError as e:
        error_reason = e
        print(f"An error occurred: {error_reason}")
        return False