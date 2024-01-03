# Copyright 2023-2024 Kazuya Onuki
# Licensed under the Apache License, Version 2.0 (the "License");
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.


import os
import logging

from logging.handlers import TimedRotatingFileHandler
from socket import gethostname
from datetime import datetime
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def create_blob_root_container(container: str, blob_service_client: BlobServiceClient):
  """if specified container does NOT exist, we create new container 

  Args:
    container (str): which you wanna create
    blob_service_client (BlobServiceClient)
  """
  container_client = blob_service_client.get_container_client(container=container)
  # Create the root container if it doesn't already exist
  if not container_client.exists():
    container_client.create_container()


class _BlobStorageFileHandler(object):
  """ it's function to authorize at blob container and get container client object.
  ref: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli

  Args:
      object (_type_): _description_
  """
  def __init__(self, account_name:str=None, container:str='instance-jupyter-logs'):
    """it's function to authorize at blob container and get container client object.
    ref: https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli

    Args:
      account_name (str, optional): storage account name to log. Defaults to None.
      container (str, optional): container name to log. Defaults to 'instance-jupyter-logs'.
    """
    try:
      # get computing host name (compute instance name etc)
      self.container:str = container
      self.account_url:str = f'https://{account_name}.blob.core.windows.net'
      
      # get azure credential
      self.default_credential = DefaultAzureCredential()
      
      # The BlobServiceClient class allows you to manipulate Azure Storage resources and blob containers.
      self.blob_service_client = BlobServiceClient(self.account_url, credential=self.default_credential)
      
      # Create the container
      create_blob_root_container(container=container, blob_service_client=self.blob_service_client)
    
    except Exception as e:
      print(f'error: {e}')
      raise(e)


  def put_file_into_storage(self, dirName:str=None, fileName:str=None):
    """it's function to upload data at blob

    Args:
      dirName (str, optional): _description_. Defaults to None.
      fileName (str, optional): _description_. Defaults to None.
    """
    try:
      file_path:str = os.path.join(dirName, fileName)      
      # Create a blob client using the local file name as the name for the blob
      self.blob_client = self.blob_service_client.get_blob_client(container=self.container, blob=fileName)
      # print(f"Uploading to Azure Storage as blob: {file_path}")
      # Upload the selected file at blob
      with open(file=file_path, mode="rb") as data:
          self.blob_client.upload_blob(data)

    except Exception as e:
      print(f'error: {e}')
      raise(e)


class BlobStorageTimedRotatingFileHandler(TimedRotatingFileHandler, _BlobStorageFileHandler):
  """
  Handler for logging to a file, rotating the log file at certain timed
  intervals.

  The outdated log file is shipped to the specified Azure Storage
  blob container and removed from the local file system immediately.
  """

  def __init__(
    self, filename, when='S', interval=1, encoding=None,
    delay=False, utc=False, account_name=None, container='instance-jupyter-logs'
  ):
    
    # TImedRotatingFileHandler class: the class to rotate log file for selected interval
    ## medhod: doRollover()
      ### execute rotation. create new logfile. if needed, delete old log file.
    ## method: emit(record)
      ### it's function to output logRecord to file. if rotation is needed, it automatically execute doRollOver.
    ## getFilesToDelete()
      ### return list of old logfile we should delete.
    TimedRotatingFileHandler.__init__(
      self,
      filename, 
      when=when,  # rotation magnitude
      interval=interval,   # rotation interval
      backupCount=1,
      encoding=encoding, 
      delay=delay, utc=utc
    )

    _BlobStorageFileHandler.__init__(self, account_name=account_name, container=container)

  def emit(self, record: logging.LogRecord):
    """it's function to output logRecord to file. if rotation is needed, it automatically execute doRollOver.

    Args:
      record (logging.LogRecord): generated instance every time we log something.
        example: record.<custom_attribute>=hoge
    """
    # set custom attribute log.
    record.hostname = gethostname().replace('_', '-')
    record.currenttime = datetime.now()
    super(BlobStorageTimedRotatingFileHandler, self).emit(record)

  def getFilesToDelete(self)->list:    
    """_summary_
    When message output is performed by the logger, the current execution time 't' is recorded.
    Comparison of the recorded time 't' with the time 't'' already recorded in <baseFilename> is done. If t - t' > interval, the doRollOver function is executed. 
    This function moves the content of <baseFilename> to <baseFilename>.<yyyy>-<mm>-<dd> <HH>:<MM>:<SS>.<mmmmmm>, and records the log for the time 't' in <baseFileName> again.
    Files to be removed with os.remove() immediately after executing doRollOver are confirmed based on the return value of getFilesToDelete().
    
    Returns:
        list: filename list you should delete when executing doRollOVer 
    """
    result = list()
    
    dirName, baseName = os.path.split(self.baseFilename)
    fileNames = os.listdir(dirName)
    baseNamelen = len(baseName)
    
    for fileName in fileNames:
      # if fileName is {baseName}.<yyyy>-<mm>-<dd> <HH>:<MM>:<SS>.<mmmmmm>
      if fileName[:baseNamelen] == baseName:
        # suffix: <yyyy>-<mm>-<dd> <HH>:<MM>:<SS>.<mmmmmm>
        suffix = fileName[(baseNamelen+1):]
        # self.extMatch: re.compile('^\\d{4}-\\d{2}-\\d{2}_\\d{2}-\\d{2}-\\d{2}(\\.\\w+)?$', re.ASCII)
        if self.extMatch.match(suffix):
          # upload to blob
          self.put_file_into_storage(dirName, fileName)
          result.append(os.path.join(dirName, fileName))
    
    # delete the stored log file from the local file system immediately
    return result