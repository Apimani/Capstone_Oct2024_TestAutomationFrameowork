import pytest
import paramiko
from sqlalchemy import create_engine
from Config.config import *  # Make sure all your config variables are imported from this file

# Fixture to create MySQL engine connection
@pytest.fixture(scope="class")
def mysql_engine():
    """Fixture to create MySQL engine connection."""
    engine = create_engine(
        f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
    )
    return engine

# Fixture to create Oracle engine connection
@pytest.fixture(scope="class")
def oracle_engine():
    """Fixture to create Oracle engine connection."""
    engine = create_engine(
        f'oracle+cx_oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}'
    )
    return engine

# Fixture for downloading sales data from Linux server using SFTP
@pytest.fixture()
def Sales_Data_From_Linux_Server():
    """Fixture to download sales data from a remote Linux server via SSH/SFTP."""
    try:
        # Establish SSH client connection
        ssh_client = paramiko.SSHClient()
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Auto accept unknown keys
        ssh_client.connect(hostname, username=username, password=password)

        # Use SFTP to download the file
        sftp = ssh_client.open_sftp()
        sftp.get(remote_file_path, local_file_path)
        print(f"File downloaded successfully from {remote_file_path} to {local_file_path}")

        yield  # The test will run after this point, and the fixture will clean up after the test finishes
        sftp.close()
        ssh_client.close()

    except Exception as e:
        print(f"An error occurred during SFTP file transfer: {e}")
        raise pytest.fail(f"Test failed due to SSH/SFTP error: {e}")

# Fixture for logging execution flow
@pytest.fixture()
def ExecutionFlow():
    """Fixture to log before and after the test steps."""
    print("Before Test Steps in execution...")
    yield  # The test will run here
    print("After Test Steps in execution...")