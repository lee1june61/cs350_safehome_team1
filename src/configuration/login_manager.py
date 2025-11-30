"""LoginManager handles user authentication and password management."""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from .exceptions import AuthenticationError
from .login_interface import LoginInterface, AccessLevel
from .storage_manager import StorageManager


class LoginManager:
    """Manages user authentication, login/logout, and password changes."""

    def __init__(
        self, storage_manager: StorageManager, *, enforce_lockout: bool = True
    ) -> None:
        self._storage_manager = storage_manager
        self._max_attempts = 3
        self._enforce_lockout = enforce_lockout

    def login(self, username: str, password: str, interface: str) -> Optional[int]:
        data = self._storage_manager.get_login_interface(username, interface)
        if not data:
            return None
        login_if = LoginInterface.from_dict(data)
        if login_if.is_locked:
            if not self._enforce_lockout:
                login_if.unlock_account()
                self._storage_manager.save_login_interface(login_if.to_dict())
            else:
                return None
        if not login_if.verify_password(password):
            login_if.increment_attempts()
            if (
                self._enforce_lockout
                and self._max_attempts > 0
                and login_if.login_attempts >= self._max_attempts
            ):
                login_if.lock_account()
            self._storage_manager.save_login_interface(login_if.to_dict())
            return None
        login_if.reset_attempts()
        login_if.last_login = datetime.utcnow()
        self._storage_manager.save_login_interface(login_if.to_dict())
        return login_if.access_level

    def logout(self) -> bool:
        return True

    def change_password(
        self, username: str, old_password: str, new_password: str, interface: str
    ) -> bool:
        data = self._storage_manager.get_login_interface(username, interface)
        if not data:
            raise AuthenticationError("User not found")
        login_if = LoginInterface.from_dict(data)
        if not login_if.verify_password(old_password):
            raise AuthenticationError("Invalid old password")
        login_if.set_password(new_password)
        self._storage_manager.save_login_interface(login_if.to_dict())
        return True

    def validate_credentials(
        self, username: str, password: str, interface: str
    ) -> bool:
        data = self._storage_manager.get_login_interface(username, interface)
        if not data:
            return False
        login_if = LoginInterface.from_dict(data)
        return login_if.verify_password(password)

    def get_access_level(self, username: str, interface: str) -> Optional[int]:
        data = self._storage_manager.get_login_interface(username, interface)
        return data.get("access_level") if data else None

    def is_account_locked(self, username: str, interface: str) -> bool:
        data = self._storage_manager.get_login_interface(username, interface)
        return bool(data.get("is_locked")) if data else False

    def configure_lockout(
        self, *, max_attempts: Optional[int] = None, enforce_lockout: Optional[bool] = None
    ):
        if max_attempts is not None and max_attempts > 0:
            self._max_attempts = max_attempts
        if enforce_lockout is not None:
            self._enforce_lockout = enforce_lockout
