import os
import shutil
import tempfile
import filecmp
import pytest

from sync_folders import sync_folder, setup_logger


@pytest.fixture
def setup_env():
    test_dir = tempfile.mkdtemp()
    source_dir = os.path.join(test_dir, "source")
    replica_dir = os.path.join(test_dir, "replica")
    os.makedirs(source_dir)
    os.makedirs(replica_dir)
    log_file = os.path.join(test_dir, "test.log")
    logger = setup_logger(log_file, log_buffer=1024, backup_count=1)

    yield source_dir, replica_dir, logger

    shutil.rmtree(test_dir)


def test_sync_new_files(setup_env):
    source_dir, replica_dir, logger = setup_env
    test_file_path = os.path.join(source_dir, "test_file.txt")

    with open(test_file_path, "w") as f:
        f.write("This is a test file.")

    sync_folder(source_dir, replica_dir, logger)
    replica_file_path = os.path.join(replica_dir, "test_file.txt")

    assert os.path.exists(replica_file_path)
    assert filecmp.cmp(test_file_path, replica_file_path)


def test_update_existing_files(setup_env):
    source_dir, replica_dir, logger = setup_env
    test_file_path = os.path.join(source_dir, "test_file.txt")

    with open(test_file_path, "w") as f:
        f.write("Original content.")

    sync_folder(source_dir, replica_dir, logger)
    replica_file_path = os.path.join(replica_dir, "test_file.txt")
    assert filecmp.cmp(test_file_path, replica_file_path)

    with open(test_file_path, "w") as f:
        f.write("Updated content.")

    sync_folder(source_dir, replica_dir, logger)
    assert filecmp.cmp(test_file_path, replica_file_path)


def test_delete_files(setup_env):
    source_dir, replica_dir, logger = setup_env
    test_file_path = os.path.join(source_dir, "test_file.txt")

    with open(test_file_path, "w") as f:
        f.write("This file will be deleted.")

    sync_folder(source_dir, replica_dir, logger)
    os.remove(test_file_path)
    sync_folder(source_dir, replica_dir, logger)

    replica_file_path = os.path.join(replica_dir, "test_file.txt")
    assert not os.path.exists(replica_file_path)
