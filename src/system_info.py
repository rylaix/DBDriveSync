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
        # Constructing the psql command to get a list of databases
        command = ['psql', '-h', host, '-p', port, '-U', user, '-t', '-c', 'SELECT datname FROM pg_database WHERE datistemplate = false;']
        print(f"Running command: {' '.join(command)}")

        # Running psql command to list databases
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        print(f"Command output: {output}")

        # Split the output by lines and strip extra spaces
        databases = [line.strip() for line in output.splitlines() if line.strip()]

    except FileNotFoundError:
        print("Error: 'psql' command not found. Please ensure PostgreSQL is installed and the 'psql' command is available in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error running psql command: {e.output}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    print(f"Databases found: {databases}")
    return databases