# DBDriveSync/src/scheduler.py

import schedule
import time
from src.system_info import list_postgres_databases
from src.backup import backup_databases
from src.gdrive_upload.py import upload_folder_to_gdrive

def run_backup_and_upload():
    """
    Run the backup and upload process.
    """
    databases = list_postgres_databases()
    if databases:
        backup_folder = backup_databases(databases)
        upload_folder_to_gdrive(backup_folder)

def schedule_backup(time_str="01:00"):
    """
    Schedule the backup process to run at a specific time every day.
    
    Args:
        time_str (str): The time to run the backup in HH:MM format.
    """
    schedule.every().day.at(time_str).do(run_backup_and_upload)

    while True:
        schedule.run_pending()
        time.sleep(1)
