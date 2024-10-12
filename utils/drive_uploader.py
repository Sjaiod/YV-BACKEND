from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import os
from decouple import config
import base64
import json


encoded_creds = config('ENCODED_GOOGLE_CREDENTIALS')

# Decode the Base64 string back to bytes, then convert it to JSON
decoded_creds = base64.b64decode(encoded_creds)
SCOPES=['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = json.loads(decoded_creds)

PARENT_FOLDER_ID = "1TP3SO5vfcnNn1DPFLqXICIhHCwebIM0W"
credentials = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build('drive', 'v3', credentials=credentials)


def authenticate():
   ## creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def upload_single_file_to_drive(file):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)

    # Metadata for the file to be uploaded
    file_metadata = {
        'name': file.name,  # Use the original file name
        'parents': [PARENT_FOLDER_ID],
    }

    # Create the file in Google Drive
    media = MediaIoBaseUpload(file, mimetype=file.content_type, resumable=True)
    file_drive = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Set the file's permissions to public
    permission = {
        'type': 'anyone',
        'role': 'reader',
    }
    service.permissions().create(fileId=file_drive['id'], body=permission).execute()

    # Get the public URL of the file
    file_url = file_drive['id']
    return file_url

def check_image_exists(image_id):
    try:
        drive_service.files().get(fileId=image_id).execute()
        return True  # Image exists
    except Exception as e:
        print(f"Error checking image existence: {e}")
        return False  # Image does not exist

# Function 2: Delete an image from Google Drive by image ID
def delete_image_from_drive(image_id):
    try:
        drive_service.files().delete(fileId=image_id).execute()
        return True  # Image deleted successfully
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False  # Failed to delete image

