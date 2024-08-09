import os
import argparse
import logging
import filecmp
import shutil
import time

from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone


class UTCFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        utc_dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        utc_dt_iso = utc_dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        
        return utc_dt_iso


def setup_logger(log_file: str, log_buffer: int, backup_count: int) -> logging.Logger:
    """
    Create and setup a formatted logger with a StreamHandler and a RotatingFileHandler attached.

    Args:
        log_file (str): Log file path (used by RotatingFileHandler)
        log_buffer (int): Max. size in bytes of each log file.
        backup_count (int): Max. number of archived log files.

    Returns:
        logging.Logger
    """

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = UTCFormatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = RotatingFileHandler(
        log_file, maxBytes=log_buffer, backupCount=backup_count, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def sync_folder(source_path: str, replica_path: str, logger: logging.Logger) -> None:
    """
    Synchronizes replica folder with source folder. Creates/updates/deletes files and dirs in
    replica based on comparison with source.

    Args:
        source_path (str): Path to source folder (source folder must exist).
        replica_path (str): Path to replica folder.
        logger (logging.Logger)
    """
    for source_dir, subdirs, filenames in os.walk(source_path):
        replica_dir = source_dir.replace(source_path, replica_path, 1)

        if not os.path.exists(replica_dir):
            os.makedirs(replica_dir)
            logger.info(f"Replica directory CREATED: {replica_dir}.")

        for filename in filenames:
            source_file = os.path.join(source_dir, filename)
            replica_file = os.path.join(replica_dir, filename)

            # I could manually use e.g. MD5 on files and compare them instead of filecmp.cmp
            # but this seems cleaner and brings the same result
            if not os.path.exists(replica_file) or not filecmp.cmp(
                source_file, replica_file
            ):
                shutil.copy2(source_file, replica_file)
                logger.info(
                    f"Source file COPIED: {source_file}. New replica: {replica_file}."
                )

    for replica_dir, subdirs, filenames in os.walk(replica_path, topdown=False):
        source_dir = replica_dir.replace(replica_path, source_path, 1)

        for filename in filenames:
            source_file = os.path.join(source_dir, filename)

            if not os.path.exists(source_file):
                replica_file = os.path.join(replica_dir, filename)
                os.remove(replica_file)
                logger.info(f"Replica file DELETED: {replica_file}.")

        if not os.path.exists(source_dir):
            os.rmdir(replica_dir)
            logger.info(f"Replica directory DELETED: {replica_dir}.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=str, help="Source folder path.")
    parser.add_argument("replica", type=str, help="Replica folder path.")
    parser.add_argument(
        "sync_interval", type=int, help="Synchronization interval in seconds."
    )
    parser.add_argument("log_file", type=str, help="Path to log file.")

    LOG_BUF_DEFAULT = 512_000
    parser.add_argument(
        "--log-buffer",
        "--lb",
        type=int,
        default=LOG_BUF_DEFAULT,
        help=f"Log file buffer size in bytes. Default: {LOG_BUF_DEFAULT}.",
    )

    BACKUP_COUNT_DEFAULT = 5
    parser.add_argument(
        "--backup-count",
        "--bc",
        type=int,
        default=BACKUP_COUNT_DEFAULT,
        help=f"Max number of archived log files. Default: {BACKUP_COUNT_DEFAULT}.",
    )

    args = parser.parse_args()

    source_path = args.source
    if not os.path.isdir(source_path):
        raise FileNotFoundError(
            f"Source folder path {source_path} is not an existing directory."
        )

    replica_path = args.replica
    sync_interval = args.sync_interval
    log_file = args.log_file
    log_buffer = args.log_buffer
    backup_count = args.backup_count

    logger = setup_logger(log_file, log_buffer, backup_count)

    while True:
        try:
            sync_folder(source_path, replica_path, logger)
            time.sleep(sync_interval)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt: folder synchronization stopped.")
            break
        except Exception as e:
            logger.error(e)
            break


if __name__ == "__main__":
    main()
