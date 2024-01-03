# PYLOGGER2AZBLOB
[![pytest](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/pytest_workflow.yaml/badge.svg)](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/pytest_workflow.yaml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![build/publish](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/publish-to-test-pypi.yaml/badge.svg)](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/publish-to-test-pypi.yaml)

## Overview
This repository provides a Python logging handler, BlobStorageTimedRotatingFileHandler, that extends the functionality of the built-in TimedRotatingFileHandler. This handler automatically rotates log files at specified intervals and uploads the outdated log files to an Azure Storage Blob container. This ensures that your log history is retained in Azure Blob Storage while keeping only the latest log on the local file system.

## Installation/Configuration

1. Install the required packages using the command:
    ```bash
    pip install azure-storage-blob
    pip install azure-identity
    pip install pylogger2azblob
    ```

1. Set an .env file with the following content:
    ```dotenv
    #######################################
    # pytest settings
    #######################################
    AZURE_BLOB_TESTLOG_FILE=pytest.log
    AZURE_BLOB_TESTLOG_DIR=./tests/testlog
    AZURE_STORAGE_TESTLOG_ACCOUNT_NAME=<your-storage-account-name>

    #######################################
    # Logging settings
    #######################################
    LOGGING_ACCOUNT_NAME=<your-storage-account-name>
    LOGGING_CONTAINER=<your-container-name>
    LOGGING_LEVEL=DEBUG
    LOGGING_FORMATTER=verbose
    LOGGING_FILENAME=./output.log
    LOGGING_WHEN=S
    LOGGING_INTERVAL=1
    ```

## Tutorial

To demonstrate how to use the logging functionality provided by PYLOGGER2AZBLOB, follow the steps below:

1. Ensure you have completed the installation steps mentioned in the [Installation/Configuration](#Installation/Configuration) section of this README.

1. To read the contents of dotenv when executing the code below, please install the following:
    ```bash
    pip install python-dotenv
    ```

1. Create a Python script, e.g., `tutorial.py`, and copy the following code:
    ```python
    import os
    import logging
    import pylogger2azblob

    from logging.config import dictConfig
    from dotenv import load_dotenv

    # Load environment variables from .env
    load_dotenv()

    LOGGING_ACCOUNT_NAME = os.getenv('LOGGING_ACCOUNT_NAME', '<your-storage-account>')
    LOGGING_CONTAINER = os.getenv('LOGGING_CONTAINER', '<your-container-name>')
    LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
    LOGGING_FORMATTER = os.getenv('LOGGING_FORMATTER', 'verbose')
    LOGGING_FILENAME = os.getenv('LOGGING_FILENAME', '<file-name-you-wanna-output>')
    LOGGING_WHEN = os.getenv('LOGGING_WHEN', 'S')
    LOGGING_INTERVAL = int(os.getenv('LOGGING_INTERVAL', 60))

    LOGGING = {
        'version': 1,
        'formatters': {
            'simple': {
                'format': '%(asctime)s %(message)s',
            },
            'verbose': {
                'format': '%(levelname)s %(hostname)s %(currenttime)s %(message)s',
            }
        },
        'handlers': {
            'blob': {
                'class': 'pylogger2azblob.handlers.BlobStorageTimedRotatingFileHandler',
                'account_name': LOGGING_ACCOUNT_NAME,
                'container': LOGGING_CONTAINER,
                'level': LOGGING_LEVEL,
                'formatter': LOGGING_FORMATTER,
                'filename': LOGGING_FILENAME,
                'when': LOGGING_WHEN,
                'interval': LOGGING_INTERVAL
            }
        },
        'loggers': {
            'example': {
                'handlers': ['blob'],
                'level': LOGGING_LEVEL,
            },
        }
    }

    dictConfig(LOGGING)
    logger = logging.getLogger('example')
    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')
    ```

1. Execute the tutorial script using the following command:
    ```bash
    python tutorial.py
    ```
    >This script configures a logger named `example` with `BlobStorageTimedRotatingFileHandler`. It logs messages with different log levels (`debug`, `info`, `warning`, `error`, and `critical`) to showcase the functionality.

1. Check the specified Azure Blob Storage container to verify that log files are created and rotated according to the specified configuration.
    <img src='./tutorial_result.png'/>
    >The result is as shown above because a dedicated storage account `kazuyalogstorage` and container name `instance-jupyter-log` were specified for testing purposes in `tutorial.py`. When you execute `tutorial.py`, please confirm that log files are placed in the corresponding container with the storage account name and container name specified on the client side.


Now, you have successfully set up and used PYLOGGER2AZBLOB to log messages and store them in Azure Blob Storage!
Feel free to customize the instructions based on your preferences or add any additional details you think are relevant.
