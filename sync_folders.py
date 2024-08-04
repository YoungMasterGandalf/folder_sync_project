import argparse


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


if __name__ == "__main__":
    main()
