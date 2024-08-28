# DBDriveSync/main.py

from src.system_info import identify_system, list_postgres_databases
from src.backup import backup_databases
from src.gdrive_upload import upload_folder_to_gdrive
from src.scheduler import schedule_backup

def main():
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

if __name__ == "__main__":
    main()
