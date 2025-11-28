"""LoginManager implementation for SafeHome.

The :class:`LoginManager` coordinates authentication-related operations
and delegates persistence to :class:`StorageManager`.
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from .exceptions import AuthenticationError
from .login_interface import LoginInterface
from .storage_manager import StorageManager
from .system_settings import SystemSettings


class LoginManager:
    """Handle user login, logout, and password management."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager
        self._current_user: Optional[str] = None
        self._current_interface: Optional[str] = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def login(self, username: str, password: str, interface: str) -> Optional[int]:
        """Attempt to log in and return access level on success.

        Args:
            username: User identifier.
            password: Plaintext password submitted by the user.
            interface: Interface identifier, e.g. "control_panel".

        Returns:
            Access level as integer if successful, otherwise ``None``.
        """
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return None

        login_if = LoginInterface.from_dict(record)
        if login_if.is_locked:
            return None

        if not self.validate_credentials(username, password, interface):
            return None

        # Successful login
        login_if.reset_attempts()
        login_if.last_login = datetime.utcnow()
        self._storage_manager.save_login_interface(login_if.to_dict())

        self._current_user = username
        self._current_interface = interface
        return int(login_if.access_level)

    def logout(self) -> bool:
        """Log out the current user, if any."""
        self._current_user = None
        self._current_interface = None
        return True

    def change_password(
        self,
        username: str,
        old_password: str,
        new_password: str,
        interface: str,
    ) -> bool:
        """Change the user's password after validating the old one."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            raise AuthenticationError("User not found.")

        login_if = LoginInterface.from_dict(record)
        if not login_if.verify_password(old_password):
            raise AuthenticationError("Old password does not match.")

        login_if.set_password(new_password)
        self._storage_manager.save_login_interface(login_if.to_dict())
        return True

    def validate_credentials(self, username: str, password: str, interface: str) -> bool:
        """Validate credentials, enforcing lockout policy."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return False

        login_if = LoginInterface.from_dict(record)
        if login_if.is_locked:
            return False

        if not login_if.verify_password(password):
            attempts = self.increment_login_attempts(username, interface)
            settings = self._load_system_settings()
            if attempts >= settings.max_login_attempts:
                login_if.lock_account()
                self._storage_manager.save_login_interface(login_if.to_dict())
            return False

        # Successful validation
        self.reset_login_attempts(username, interface)
        return True

    def get_access_level(self, username: str, interface: str) -> Optional[int]:
        """Return the access level for the given user/interface."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return None
        login_if = LoginInterface.from_dict(record)
        return int(login_if.access_level)

    def increment_login_attempts(self, username: str, interface: str) -> int:
        """Increment failed login attempts and persist."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return 0
        login_if = LoginInterface.from_dict(record)
        attempts = login_if.increment_attempts()
        self._storage_manager.save_login_interface(login_if.to_dict())
        return attempts

    def reset_login_attempts(self, username: str, interface: str) -> bool:
        """Reset failed login attempts and persist."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return False
        login_if = LoginInterface.from_dict(record)
        login_if.reset_attempts()
        login_if.unlock_account()
        self._storage_manager.save_login_interface(login_if.to_dict())
        return True

    def is_account_locked(self, username: str, interface: str) -> bool:
        """Return True if the account is locked."""
        record = self._storage_manager.get_login_interface(username, interface)
        if record is None:
            return False
        login_if = LoginInterface.from_dict(record)
        return login_if.is_locked

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    def _load_system_settings(self) -> SystemSettings:
        """Load system settings from the database with defaults."""
        settings = SystemSettings()
        settings.load_from_database(self._storage_manager)
        return settings



