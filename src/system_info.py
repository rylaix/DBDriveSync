# DBDriveSync/src/system_info.py

import os
import platform
import subprocess
import configparser

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
    base_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_dir, '..', 'config.ini')  # Adjust path to point to base directory

    print(f"Loading configuration from: {config_path}")

    # Check if the config file exists
    if not os.path.exists(config_path):
        print(f"Error: Configuration file {config_path} not found.")
        return []

    # Load the configuration file
    config = configparser.ConfigParser()
    config.read(config_path)

    # Ensure the POSTGRESQL section is present
    if 'POSTGRESQL' not in config:
        print("Error: 'POSTGRESQL' section not found in config.ini.")
        return []

    # Read PostgreSQL credentials from config file
    host = config['POSTGRESQL']['HOST']
    port = config['POSTGRESQL']['PORT']
    user = config['POSTGRESQL']['USER']
    password = config['POSTGRESQL']['PASSWORD']

    # Set the password environment variable
    os.environ['PGPASSWORD'] = password

    system = identify_system()
    databases = []

    try:
        # Running psql command to list databases
        output = subprocess.check_output(['psql', '-h', host, '-p', port, '-U', user, '-l'], universal_newlines=True)
        for line in output.splitlines():
            if '|' in line and not line.startswith(' '):
                db = line.split('|')[0].strip()
                databases.append(db)
    except FileNotFoundError as e:
        print("Error: 'psql' command not found. Please ensure PostgreSQL is installed and the 'psql' command is available in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error listing databases: {e.output}")
    except Exception as e:
        print(f"Error listing databases: {e}")
    
    return databases
