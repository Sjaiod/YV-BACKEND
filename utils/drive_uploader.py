# from googleapiclient.discovery import build
# from google.oauth2 import service_account
# from googleapiclient.http import MediaIoBaseUpload
# import os
# from decouple import config
# import json


# SCOPES=['https://www.googleapis.com/auth/drive']
# ##SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), config("GOOGLE_SERVICE_ACCOUNT_JSON"))
# SERVICE_ACCOUNT_FILE = json.loads(config("GOOGLE_SERVICE_ACCOUNT_JSON"))
# PARENT_FOLDER_ID = "1TP3SO5vfcnNn1DPFLqXICIhHCwebIM0W"
# credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
# drive_service = build('drive', 'v3', credentials=credentials)


# def authenticate():
#     creds = service_account.Credentials.from_service_account_info(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
#     return creds

# def upload_single_file_to_drive(file):
#     creds = authenticate()
#     service = build('drive', 'v3', credentials=creds)

#     # Metadata for the file to be uploaded
#     file_metadata = {
#         'name': file.name,  # Use the original file name
#         'parents': [PARENT_FOLDER_ID],
#     }

#     # Create the file in Google Drive
#     media = MediaIoBaseUpload(file, mimetype=file.content_type, resumable=True)
#     file_drive = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

#     # Set the file's permissions to public
#     permission = {
#         'type': 'anyone',
#         'role': 'reader',
#     }
#     service.permissions().create(fileId=file_drive['id'], body=permission).execute()

#     # Get the public URL of the file
#     file_url = file_drive['id']
#     return file_url

# def check_image_exists(image_id):
#     try:
#         drive_service.files().get(fileId=image_id).execute()
#         return True  # Image exists
#     except Exception as e:
#         print(f"Error checking image existence: {e}")
#         return False  # Image does not exist

# # Function 2: Delete an image from Google Drive by image ID
# def delete_image_from_drive(image_id):
#     try:
#         drive_service.files().delete(fileId=image_id).execute()
#         return True  # Image deleted successfully
#     except Exception as e:
#         print(f"Error deleting image: {e}")
#         return False  # Failed to delete image

from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseUpload
import os
from decouple import config
import json

# Define scopes and load credentials from the environment variable
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = os.path.join(os.path.dirname(__file__), "service_account.json")
PARENT_FOLDER_ID = "1TP3SO5vfcnNn1DPFLqXICIhHCwebIM0W"

# Create credentials from the JSON info (since it's not a file)
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Initialize the Drive service
drive_service = build('drive', 'v3', credentials=credentials)


def authenticate():
    # This function is no longer needed as the credentials are already created globally
    return credentials


def upload_single_file_to_drive(file):
    # Use global credentials to avoid re-authentication
    service = drive_service

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

    # Get the file ID (public URL is based on file ID)
    file_url = f"https://drive.google.com/file/d/{file_drive['id']}/view?usp=sharing"
    return file_url


def check_image_exists(image_id):
    try:
        drive_service.files().get(fileId=image_id).execute()
        return True  # Image exists
    except Exception as e:
        print(f"Error checking image existence: {e}")
        return False  # Image does not exist


# Function to delete an image from Google Drive by image ID
def delete_image_from_drive(image_id):
    try:
        drive_service.files().delete(fileId=image_id).execute()
        return True  # Image deleted successfully
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False  # Failed to delete image