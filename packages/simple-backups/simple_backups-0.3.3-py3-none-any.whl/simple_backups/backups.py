import logging
import shutil
from datetime import datetime
from pathlib import Path

from .exceptions import SimpleBackupsError

logger = logging.getLogger(__name__)


# TODO Add support for Python 3.9??
# TODO Add zipping capabilities
# TODO Add zipping folder capabilities
# TODO Add async capabilities.
# TODO Add documentations


def backup_file(
    filename: Path,
    backup_folder: Path,
    datetime_format: str = '%Y%m%d_%H%M%S',
    current_version: str = None,
) -> Path:
    """
    Copies the filename to the backup folder append the datetime and version if supplied
    @param filename: The name of the file to backup.
    @param backup_folder: The folder where the backup will be stored.
    @param datetime_format: The datetime format to include in the backup file.
    @param current_version: The version of the application.
    @return: The path to the backup file.
    """
    if not backup_folder.is_dir():
        error_message = f'Backup folder has to be a folder.' f' Supplied: {backup_folder}. Type: {type(backup_folder)}'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)

    backup_filename = build_filename(
        file_path=filename,
        backup_folder=backup_folder,
        current_version=current_version,
        datetime_format=datetime_format,
    )
    if backup_filename == filename:
        error_message = f'Cannot overwrite backup file: {backup_filename}.'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)
    try:
        shutil.copy(filename, backup_filename)
        return backup_filename
    except Exception as e:
        error_message = f'Unexpected error backing up file {filename}. Type: {e.__class__.__name__}' f' error: {e}'
        logger.error(error_message)
        raise SimpleBackupsError(error_message)


def build_filename(
    *, file_path: Path, backup_folder: Path, current_version: str | None, datetime_format: str | None
) -> Path:
    """
    Hello
    Args:
        file_path: c
        backup_folder: c
        current_version: c
        datetime_format: c

    Returns: gg

    """
    if current_version is None:
        version_val = ''
    else:
        version_val = f'v{current_version}_'
    if datetime_format is None:
        timestamp_val = ''
    else:
        timestamp = datetime.now().strftime(datetime_format)
        timestamp_val = f'{timestamp}_'
    backup_filename = backup_folder / f'{timestamp_val}{version_val}{file_path.name}'
    return backup_filename
