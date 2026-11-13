
import hashlib
from pathlib import Path

from PySide6.QtCore import QStandardPaths


def get_app_data_directory():
    """
    Return LogicFlow's writable application data directory.

    This directory is outside the installed application, so
    user data remains available when the application is updated.
    """

    location = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.AppLocalDataLocation
    )

    if not location:
        raise RuntimeError(
            "Could not locate LogicFlow's application data directory."
        )

    app_data_directory = Path(location)
    app_data_directory.mkdir(parents=True, exist_ok=True)

    return app_data_directory


def get_account_storage_directory(username):
    """
    Return the storage directory belonging to a username.

    Each account receives its own directory, identified by
    a SHA-256 hash of its normalized username.
    """

    if not isinstance(username, str) or not username.strip():
        raise ValueError("A valid username is required.")

    normalized_username = username.strip().casefold()

    account_id = hashlib.sha256(
        normalized_username.encode("utf-8")
    ).hexdigest()

    accounts_directory = get_app_data_directory() / "accounts"

    account_directory = accounts_directory / account_id

    account_directory.mkdir(parents=True, exist_ok=True)

    return account_directory
