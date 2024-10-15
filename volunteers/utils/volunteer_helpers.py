import pandas as pd
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils.drive_uploader import authenticate
import datetime
import openpyxl

def create_new_volunteer_sheet():
    # Define the columns for the new volunteer sheet
    columns = ["Name", "Email", "Phone", "Age", "T-shirt Size", "Registration Date", "Blood Group", "Payment ID"]

    # Create an empty DataFrame with the specified columns
    df = pd.DataFrame(columns=columns)

    # Create a unique file name using the current timestamp
    file_name = f'volunteers_{pd.Timestamp.now().strftime("%Y-%m-%d_%H-%M-%S")}.xlsx'

    # Define the directory where the file will be saved (e.g., a 'sheets' folder inside the 'volunteers' app)
    sheets_dir = os.path.join(os.getcwd(), 'volunteers', 'sheets')

    # Create the directory if it doesn't exist
    if not os.path.exists(sheets_dir):
        os.makedirs(sheets_dir)

    # Save the new Excel file to the defined directory
    file_path = os.path.join(sheets_dir, file_name)
    df.to_excel(file_path, index=False)

    # Path to the text file that will store the latest file name
    path_file = os.path.join(sheets_dir, 'path.txt')

    # Check if the path file exists
    if os.path.exists(path_file):
        # If the file exists, clear its contents
        with open(path_file, 'w') as f:
            f.write(file_name)
    else:
        # If the file doesn't exist, create it and write the file name
        with open(path_file, 'w') as f:
            f.write(file_name)

    return file_name  # Return just the file name




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
        'role': 'reader',
    }
    service.permissions().create(fileId=uploaded_file['id'], body=permission).execute()

    # Generate the public URL for the file
    file_url = f"https://drive.google.com/uc?export=view&id={uploaded_file['id']}"

    return file_url

# Function to append new volunteer data to the existing Excel sheet
def append_to_volunteer_sheet(data):
    try:
        current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Get the path of the Excel sheet from path.txt
        sheets_dir = os.path.join(os.getcwd(), 'volunteers', 'sheets')
        path_file = os.path.join(sheets_dir, 'path.txt')
        
        if not os.path.exists(path_file):
            print("No active volunteer sheet found.")
            return "No active volunteer sheet found."
        
        with open(path_file, 'r') as f:
            file_name = f.read().strip()
            print(file_name)

        # Full path to the Excel file
        file_path = os.path.join(sheets_dir, file_name)
        
        # Load the existing Excel sheet
        wb = openpyxl.load_workbook(file_path)
        ws = wb.active

        # If it's a new sheet (headers might be missing), add them
        if ws.max_row == 1:
            headers = ["Name", "Email", "Phone", "Age", "T-shirt Size", "Registration Date", "Blood Group", "Payment ID"]
            ws.append(headers)

        # Append new volunteer data to the sheet
        new_row = [
            data.get('name'),
            data.get('email'),
            data.get('phone'),
            data.get('age'),
            data.get('tshirt_size'),
            current_time,  # Registration date
            data.get('blood_group'),
            data.get('payment_id')
        ]

        ws.append(new_row)

        # Save the updated workbook
        wb.save(file_path)

        return True
    except Exception as e:
        print(f"Error while appending to sheet: {e}")
        return False