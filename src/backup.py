# DBDriveSync/src/backup.py

import os
import subprocess
from datetime import datetime
import configparser

def create_backup_folder():
    """
    Create a backup folder with the current date.
    
    Returns:
        str: Path to the backup folder.
    """
    backup_folder = os.path.join("backups", datetime.now().strftime("%Y-%m-%d"))
    os.makedirs(backup_folder, exist_ok=True)
    return backup_folder

def backup_database(db_name, backup_folder):
    """
    Backup a single PostgreSQL database.
    
    Args:
        db_name (str): The name of the database to backup.
        backup_folder (str): The folder where the backup will be stored.
        
    Returns:
        str: The path to the backup file.
    """
    config = configparser.ConfigParser()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, '..', 'config.ini')
    config.read(config_path)

    host = config['POSTGRESQL']['HOST']
    port = config['POSTGRESQL']['PORT']
    user = config['POSTGRESQL']['USER']
    password = config['POSTGRESQL']['PASSWORD']

    # Set the password environment variable for pg_dump
    os.environ['PGPASSWORD'] = password

    backup_file = os.path.join(backup_folder, f"{db_name}.sql")
    try:
        subprocess.check_call(['pg_dump', '-h', host, '-p', port, '-U', user, '-Fc', '-f', backup_file, db_name])
        print(f"Database {db_name} backed up successfully to {backup_file}")
    except Exception as e:
        print(f"Error backing up {db_name}: {e}")
    return backup_file

def backup_databases(databases):
    """
    Backup multiple PostgreSQL databases.
    
    Args:
        databases (list): A list of database names to backup.
        
    Returns:
        list: A list of paths to the backup files.
    """
    backup_folder = create_backup_folder()
    backup_files = []

    for db in databases:
        backup_file = backup_database(db, backup_folder)
        backup_files.append(backup_file)

    return backup_folder
