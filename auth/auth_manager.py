
import hashlib
import hmac
import json
import re
import secrets

from pathlib import Path

from PySide6.QtCore import QStandardPaths


class AuthManager:
    """Manage offline LogicFlow accounts securely."""

    PBKDF2_ITERATIONS = 600_000
    SALT_SIZE = 16

    USERNAME_PATTERN = re.compile(
        r"^[A-Za-z0-9_.-]{3,24}$"
    )

    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128

    def __init__(self):
        app_data = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppLocalDataLocation
        )

        if not app_data:
            raise RuntimeError(
                "Could not locate the application data directory."
            )

        self.data_directory = Path(app_data)
        self.data_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.data_file = self.data_directory / "accounts.json"

        self.data = self._load_data()

    def _default_data(self):
        return {
            "version": 1,
            "accounts": {},
            "remembered_username": ""
        }

    def _load_data(self):
        """Load account data without silently overwriting corrupt files."""

        if not self.data_file.exists():
            return self._default_data()

        try:
            with self.data_file.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("Invalid account data.")

            accounts = data.get("accounts", {})

            if not isinstance(accounts, dict):
                raise ValueError("Invalid accounts section.")

            return {
                "version": 1,
                "accounts": accounts,
                "remembered_username": str(
                    data.get("remembered_username", "")
                )
            }

        except (OSError, json.JSONDecodeError, ValueError) as error:
            raise RuntimeError(
                "LogicFlow could not read its local account file. "
                "Your existing data has not been overwritten."
            ) from error

    def _save_data(self):
        """Save data using an atomic file replacement."""

        temporary_file = self.data_file.with_suffix(".tmp")

        try:
            with temporary_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    self.data,
                    file,
                    indent=4
                )

                file.flush()

            temporary_file.replace(self.data_file)

        except OSError:
            if temporary_file.exists():
                try:
                    temporary_file.unlink()
                except OSError:
                    pass

            raise

    @staticmethod
    def _username_key(username):
        return username.strip().casefold()

    def validate_username(self, username):
        username = username.strip()

        if not self.USERNAME_PATTERN.fullmatch(username):
            return (
                False,
                "Username must be 3–24 characters and contain "
                "only letters, numbers, dots, hyphens or underscores."
            )

        return True, ""

    def validate_password(self, password):
        if len(password) < self.MIN_PASSWORD_LENGTH:
            return (
                False,
                "Password must contain at least 8 characters."
            )

        if len(password) > self.MAX_PASSWORD_LENGTH:
            return (
                False,
                "Password cannot exceed 128 characters."
            )

        return True, ""

    def _hash_password(self, password, salt):
        return hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self.PBKDF2_ITERATIONS
        )

    def has_accounts(self):
        return bool(self.data["accounts"])

    def create_account(self, username, password):
        """Create a new local account."""

        username = username.strip()

        valid, message = self.validate_username(username)

        if not valid:
            return False, message

        valid, message = self.validate_password(password)

        if not valid:
            return False, message

        key = self._username_key(username)

        if key in self.data["accounts"]:
            return False, "That username is already registered."

        salt = secrets.token_bytes(self.SALT_SIZE)
        password_hash = self._hash_password(password, salt)

        self.data["accounts"][key] = {
            "username": username,
            "salt": salt.hex(),
            "password_hash": password_hash.hex(),
            "iterations": self.PBKDF2_ITERATIONS
        }

        try:
            self._save_data()

        except OSError:
            del self.data["accounts"][key]

            return (
                False,
                "Could not save your account. Check folder permissions."
            )

        return True, "Account created successfully."

    def authenticate(self, username, password):
        """Verify a username and password."""

        key = self._username_key(username)

        account = self.data["accounts"].get(key)

        if account is None:
            return False, "Invalid username or password."

        try:
            salt = bytes.fromhex(account["salt"])
            stored_hash = bytes.fromhex(
                account["password_hash"]
            )

            iterations = int(
                account.get(
                    "iterations",
                    self.PBKDF2_ITERATIONS
                )
            )

            if not 100_000 <= iterations <= 1_000_000:
                return False, "Invalid account data."

            calculated_hash = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations
            )

        except (KeyError, ValueError, TypeError, UnicodeError):
            return False, "Invalid account data."

        if not hmac.compare_digest(
            stored_hash,
            calculated_hash
        ):
            return False, "Invalid username or password."

        return True, account["username"]

    def get_remembered_username(self):
        return self.data.get("remembered_username", "")

    def set_remembered_username(self, username):
        """Remember only the username, never the password."""

        self.data["remembered_username"] = username.strip()

        try:
            self._save_data()
            return True

        except OSError:
            return False
