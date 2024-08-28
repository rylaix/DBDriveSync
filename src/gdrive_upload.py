# DBDriveSync/src/gdrive_upload.py

import os
import configparser
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def load_gdrive_config():
    """
    Load Google Drive configuration from config file.
    
    Returns:
        tuple: Credentials object and backup folder ID.
    """
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    credentials = service_account.Credentials.from_service_account_file(
        config['GOOGLE_DRIVE']['CREDENTIALS_FILE'],
        scopes=['https://www.googleapis.com/auth/drive.file']
    )
    folder_id = config['GOOGLE_DRIVE']['BACKUP_FOLDER_ID']
    return credentials, folder_id

def upload_folder_to_gdrive(folder):
    """
    Upload the backup folder to Google Drive.
    
    Args:
        folder (str): The path to the folder to upload.
    """
    credentials, folder_id = load_gdrive_config()
    service = build('drive', 'v3', credentials=credentials)
    
    # Create a new folder in Google Drive
    file_metadata = {
        'name': os.path.basename(folder),
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [folder_id]
    }
    created_folder = service.files().create(body=file_metadata, fields='id').execute().get('id')
    
    # Upload each file in the folder
    for root, dirs, files in os.walk(folder):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            media = MediaFileUpload(file_path, resumable=True)
            file_metadata = {
                'name': file_name,
                'parents': [created_folder]
            }
            service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    print(f"Backup folder {folder} uploaded to Google Drive")
