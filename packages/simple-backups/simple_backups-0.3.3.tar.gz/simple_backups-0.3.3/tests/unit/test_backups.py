from freezegun import freeze_time

from simple_backups.backups import backup_file, build_filename


@freeze_time("2023-01-01 12:00:00")  # Set a fixed datetime for testing
def test_backup_file(tmp_path):
    # Create a temporary file for testing
    test_file = tmp_path / "test_file.txt"
    test_file.write_text("Test content")

    # Create a backup folder
    backup_folder = tmp_path / "backup"
    backup_folder.mkdir()

    backup_path = backup_file(test_file, backup_folder)

    # Check if the backup file has the expected format
    assert backup_path.name.startswith("20230101_120000_")
    assert backup_path.parent == backup_folder
    # Mock the shutil.copy method to avoid actual file copying
    # with patch("shutil.copy") as mock_copy:
    #     # Perform the backup
    #     backup_path = backup_file(test_file, backup_folder)

    #     # Check if the backup file has the expected format
    #     assert backup_path.name.startswith("20230101_120000_")
    #     assert backup_path.parent == backup_folder

    # Verify that shutil.copy was called with the correct arguments
    #  mock_copy.assert_called_once_with(test_file, backup_path)


@freeze_time("2023-01-01 12:00:00")  # Set a fixed datetime for testing
def test_build_filename(tmp_path):
    # Create a temporary file path for testing
    test_file = tmp_path / "test_file.txt"

    # Create a backup folder
    backup_folder = tmp_path / "backup"
    backup_folder.mkdir()

    # Test without current_version and datetime_format
    backup_filename = build_filename(
        file_path=test_file, backup_folder=backup_folder, current_version=None, datetime_format=None
    )
    assert backup_filename.name == "test_file.txt"

    # Test with current_version and datetime_format
    backup_filename = build_filename(
        file_path=test_file, backup_folder=backup_folder, current_version="1.0", datetime_format="%Y%m%d_%H%M%S"
    )
    assert backup_filename.name.startswith("20230101_120000_v1.0_test_file.txt")

    # Test with current_version and without datetime_format
    backup_filename = build_filename(
        file_path=test_file, backup_folder=backup_folder, current_version="1.0", datetime_format=None
    )
    assert backup_filename.name.startswith("v1.0_test_file.txt")

    # Test without current_version and with datetime_format
    backup_filename = build_filename(
        file_path=test_file, backup_folder=backup_folder, current_version=None, datetime_format="%Y%m%d_%H%M%S"
    )
    assert backup_filename.name.startswith("20230101_120000_test_file.txt")
