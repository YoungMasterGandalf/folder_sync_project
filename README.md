# Folder Sync Project

## Overview

This Python project is a utility designed to synchronize a replica folder with a source folder. The 
utility compares the contents of the source and replica folders, copying, updating, or deleting 
files and directories in the replica folder to ensure it mirrors the source folder. The 
synchronization runs continuously at specified intervals, making it ideal for tasks that require 
consistent backup or mirroring of directory contents.

## Features

- **Folder Synchronization:** Automatically synchronizes files and directories from the source 
folder to the replica folder.
- **Efficient Comparison:** Uses file comparison (via `filecmp.cmp`) to ensure files are only copied 
if they differ from the source.
- **Logging:** Comprehensive logging of synchronization activities, including file and directory 
creations, updates, and deletions.
- **Rotating Logs:** Utilizes rotating file handlers to manage log files, ensuring that log storage 
is efficient and old logs are archived.
- **Interrupt Handling:** Gracefully stops synchronization upon receiving a keyboard interrupt.

## Installation

Clone this repository and ensure Python 3.6 or higher is installed on your machine. No external 
packages are required beyond Python's standard library.

```bash
git clone https://github.com/YoungMasterGandalf/folder_sync_project
cd folder_sync_project
```

## Usage

To run the utility, use the following command:

```bash
python sync_folders.py <source_folder> <replica_folder> <sync_interval> <log_file> [--log-buffer LOG_BUFFER] [--backup-count BACKUP_COUNT]
```

- `<source_folder>`: Path to the source folder.
- `<replica_folder>`: Path to the replica folder.
- `<sync_interval>`: Time interval (in seconds) between synchronization checks.
- `<log_file>`: Path to the log file.

Optional arguments:
- `--log-buffer` or `--lb`: Set the log file buffer size in bytes (default: 512,000 bytes).
- `--backup-count` or `--bc`: Set the maximum number of archived log files (default: 5).

To see all the possible arguments and their explanation, use:

```bash
python sync_folders.py -h
```

### Example

```bash
python sync_folders.py /path/to/source /path/to/replica 300 sync.log --log-buffer 1000000 --backup-count 3
```

This command synchronizes the replica folder with the source folder every 300 seconds (5 minutes) 
and logs the activity in `sync.log`. The log file size is capped at 1 MB, and up to 3 old log files 
are archived.

## Run with Docker

Note: Docker image is not yet uploaded on DockerHub - TBD.

To create your local Docker image run:

```bash
docker build -t <image_name>:<version_tag> .
```

Follow by creating a container from this image with:

```bash
docker run -d --name <new_container_name> -v <host_src_dir>:<cont_src_dir> -v <host_repl_dir>:<cont_repl_dir> -v <host_log_file>:<cont_log_file> <docker_image_name> <cont_src_dir> <cont_repl_dir> <cont_log_file> [--log-buffer LOG_BUFFER] [--backup-count BACKUP_COUNT] 
```
