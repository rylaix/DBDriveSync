# DBDriveSync/src/system_info.py

import platform
import subprocess

def identify_system():
    """
    Identify the operating system.
    
    Returns:
        str: The name of the operating system.
    """
    return platform.system()

def list_postgres_databases():
    """
    List all PostgreSQL databases on the system.
    
    Returns:
        list: A list of database names.
    """
    system = identify_system()
    databases = []
    
    try:
        # Running psql command to list databases
        output = subprocess.check_output(['psql', '-l'], universal_newlines=True)
        for line in output.splitlines():
            if '|' in line and not line.startswith(' '):
                db = line.split('|')[0].strip()
                databases.append(db)
    except Exception as e:
        print(f"Error listing databases: {e}")
    
    return databases
