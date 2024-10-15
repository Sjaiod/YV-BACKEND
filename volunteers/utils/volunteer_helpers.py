import pandas as pd
import os
from googleapiclient.discovery import build
import io
from googleapiclient.http import MediaFileUpload
from utils.drive_uploader import authenticate
import datetime

def create_new_volunteer_sheet():
    # Define the columns for the new volunteer sheet
    columns = ["Name", "Email", "Phone","Age","T-shirt Size" "Registration Date","Blood Group"]

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

    return file_path  # Return the path to the created Excel file



def stop_volunteer_intake(file_path):
    # Authenticate with Google Drive
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    PARENT_FOLDER_ID="1IBi1xdLWsfKY99ZsSBgoMeiFC6REvO_E"

    # Metadata for the file to be uploaded
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_metadata = {
        'name': f'Volunteer_Sheet_{current_time}.xlsx',   # You can change this to something dynamic like file name
        'parents': [PARENT_FOLDER_ID],  # Folder ID in Google Drive where the file will be uploaded
    }

    # Create the file in Google Drive
    media = MediaFileUpload(file_path, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Set permissions for the file to make it public
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=uploaded_file['id'], body=permission).execute()

    # Generate the public URL of the uploaded file
    file_url = f"https://drive.google.com/uc?export=view&id={uploaded_file['id']}"

    return file_url