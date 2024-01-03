import os
import tempfile
import logging
import pytest
import uuid

from socket import gethostname
from datetime import datetime
from dotenv import load_dotenv
from pylogger2azblob.handlers import BlobStorageTimedRotatingFileHandler


# read environment variable from .env
load_dotenv()

file_name = os.getenv('AZURE_BLOB_TESTLOG_FILE')
testlog_dir = os.getenv('AZURE_BLOB_TESTLOG_DIR', './tests/testlog')
account_name = os.getenv('AZURE_STORAGE_TESTLOG_ACCOUNT_NAME', '<your-storage-account-name>')

os.makedirs(testlog_dir, exist_ok=True)
file_path = f'{testlog_dir}/{file_name}'
test_old_log_file_name = f'{file_name}.2000-01-01_00-00-00'
test_old_log_file_path = f'{testlog_dir}/{test_old_log_file_name}'
container = f'pytest-{uuid.uuid1()}'


"""
In pytest, fixtures default to the function scope, resulting in the creation of a new instance for each test function. 
By using the scope option, you can control the lifespan and scope of the fixture. 
Specifically, specifying scope="session" ensures that the fixture is created only once for the entire test session, allowing it to be shared across all test functions.
"""
@pytest.fixture(scope="session")
def blob_handler(request):
  print(f'\ncontainer name: {container}')
  handler = BlobStorageTimedRotatingFileHandler(
    filename=file_path, 
    account_name=account_name,
    container=container
  )
  yield handler
  
  # NOTE: delete container/blob logic after test session ended.
  container_client = handler.blob_service_client.get_container_client(container)
  
  try:
    container_client.delete_container()
    print(f"\nContainer '{container}' deleted successfully.")
  
  except Exception as e:
    print(f"\nError deleting container '{container}': {e}")


def test_emit(blob_handler):
  record = logging.LogRecord(
    name=file_name,
    pathname=file_name,
    lineno=1,
    args=None,
    exc_info=None,
    level=logging.INFO,
    hostname=gethostname().replace('_', '-'),
    currenttime=datetime.now(),
    msg="Test message"
  )
  blob_handler.emit(record)

  # check where local log file exists.
  assert os.path.isfile(file_path), f"Pytest log file {file_path} does not exist."

  # check whegher container exists or not.
  container_client = blob_handler.blob_service_client.get_container_client(container)
  container_exists = container_client.exists()
  assert container_exists, f"Container '{container}' does not exist in Azure Blob Storage."


def test_get_files_to_delete(blob_handler):
  with open(test_old_log_file_path, 'w') as f:
    f.write('test old message')

  deleted_files = blob_handler.getFilesToDelete()
  
  blob_client = blob_handler.blob_service_client.get_blob_client(
    container=container, blob=test_old_log_file_name)
  blob_exists = blob_client.exists()
  # check where blob exists.
  assert blob_exists, f"Blob '{test_old_log_file_name}' does not exist in Azure Blob Storage."
  assert isinstance(deleted_files, list), f'getFilesToDelete() does not return list type'
  os.remove(test_old_log_file_path)


def test_put_file_into_storage(blob_handler):
  with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    temp_file.write(b"test content")
    temp_file_path = temp_file.name
    dirName = os.path.dirname(temp_file_path)
    fileName = os.path.basename(temp_file_path)
  
  try:
    blob_handler.put_file_into_storage(dirName, fileName)
    # check where blob exists
    blob_client = blob_handler.blob_service_client.get_blob_client(
      container=container, blob=fileName)
    blob_exists = blob_client.exists()
    assert blob_exists, f"Blob '{fileName}' does not exist in Azure Blob Storage."
  
  finally:
    os.remove(temp_file_path)