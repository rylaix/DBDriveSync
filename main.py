# DBDriveSync/main.py
import os
import webbrowser

from src.system_info import identify_system, list_postgres_databases
from src.backup import backup_databases
from src.gdrive_upload import upload_folder_to_gdrive
from src.scheduler import schedule_backup

def main():
    check_or_create_credentials()

    # Proceed with the rest of your application logic
    print("Proceeding with the backup process...")
    
    print(f"Running on {identify_system()} system.")
    
    # Get list of PostgreSQL databases
    databases = list_postgres_databases()
    
    if not databases:
        print("No PostgreSQL databases found.")
        return
    
    # Backup databases
    backup_folder = backup_databases(databases)
    
    # Upload backup to Google Drive
    upload_folder_to_gdrive(backup_folder)
    
    # Schedule periodic backups
    schedule_backup()

def check_or_create_credentials():
    credentials_path = os.path.join("config", "credentials.json")

    if not os.path.exists(credentials_path):
        print("Google Drive API credentials not found!")
        print("You need to create 'credentials.json' in the 'config' directory.")
        print("Follow these steps to create the credentials file:")

        instructions = """
        1. Go to the Google Cloud Console: https://console.developers.google.com/
        2. Create a new project (or select an existing one).
        3. Enable the Google Drive API for your project.
        4. Go to 'Credentials' and create a new OAuth 2.0 Client ID.
           - Application type: Desktop app
        5. Download the JSON file and save it as 'credentials.json'.
        6. Place the 'credentials.json' file in the 'config' directory.
        """

        print(instructions)
        
        # Optionally open the Google Cloud Console in the default web browser
        open_browser = input("Would you like to open the Google Cloud Console in your browser? (y/n): ").strip().lower()
        if open_browser == 'y':
            webbrowser.open("https://console.developers.google.com/")

        input("Press Enter after you have placed 'credentials.json' in the 'config' directory.")
        
        if not os.path.exists(credentials_path):
            print("The 'credentials.json' file was not found. Please follow the instructions to create it.")
            exit(1)
    else:
        print("Google Drive API credentials found.")

if __name__ == "__main__":
    main()
