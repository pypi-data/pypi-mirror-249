# PYLOGGER2AZBLOB
[![pytest](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/pytest_workflow.yaml/badge.svg)](https://github.com/KazuOnuki/pylogger2azblob/actions/workflows/pytest_workflow.yaml)
[![License](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

## Overview
This repository provides a Python logging handler, BlobStorageTimedRotatingFileHandler, that extends the functionality of the built-in TimedRotatingFileHandler. This handler automatically rotates log files at specified intervals and uploads the outdated log files to an Azure Storage Blob container. This ensures that your log history is retained in Azure Blob Storage while keeping only the latest log on the local file system.


Please note, the `PYLOGGER2AZBLOB` is now open source! 
The repo is available here: [PYLOGGER2AZBLOB - Github](https://github.com/KazuOnuki/pylogger2azblob).

## Changelog
### 0.1.0 (2024-01-03)
- first release