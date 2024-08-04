import os
import argparse
import logging
import filecmp
import shutil
import time


def main():
    parser = argparse.ArgumentParser()

    source_help = "Source folder path, e.g. '/Users/JohnDoe/Documents/source'."
    parser.add_argument("source", type=str, help=source_help)

    replica_help = (
        "Replica folder path, e.g. '/Users/JohnDoe/Documents/source_replica'."
    )
    parser.add_argument("replica", type=str, help=replica_help)

    sync_interval_help = "Synchronization interval in seconds, e.g. '5' will result in sync each 5 seconds."
    parser.add_argument("sync_interval", type=int, help=sync_interval_help)

    log_file_help = "Path to a file storing the log output, e.g. '/Users/JohnDoe/Documents/logs.json'."
    parser.add_argument("log_file", type=str, help=log_file_help)

    args = parser.parse_args()

    source_path = args.source
    if not os.path.isdir(source_path):
        raise FileNotFoundError(
            f"Source folder path {source_path} is not an existing directory."
        )

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    console_handler = logging.StreamHandler()
    logger.addHandler(console_handler)

    replica_path = args.replica
    sync_interval = args.sync_interval
    log_file = args.log_file

    while True:
        try:
            for source_dir, subdirs, filenames in os.walk(source_path):
                replica_dir = source_dir.replace(source_path, replica_path, 1)

                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logger.info(f"Replica directory CREATED: {replica_dir}.")

                for filename in filenames:
                    source_file = os.path.join(source_dir, filename)
                    replica_file = os.path.join(replica_dir, filename)

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

            time.sleep(sync_interval)
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt: folder synchronization stopped.")
            break
        except Exception as e:
            logger.error(e)
            break


if __name__ == "__main__":
    main()
