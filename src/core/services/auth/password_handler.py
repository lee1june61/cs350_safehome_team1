"""Password change and verification handlers."""

from __future__ import annotations

from typing import Dict, Optional

from ....configuration import LoginInterface, StorageManager
from .lock_manager import LockManager


class PasswordChangeHandler:
    """Handles password change logic."""

    def __init__(self, login_manager, logger, lock_manager: LockManager):
        self._login_manager = login_manager
        self._logger = logger
        self._lock = lock_manager

    def change(
        self,
        current_user: Optional[str],
        username: str,
        current_password: str,
        new_password: str,
        interface: str,
        ensure_auth_fn,
    ) -> Dict:
        target_user = username or "master"
        if not current_user:
            if not ensure_auth_fn(target_user, current_password, interface):
                return {"success": False, "message": "Must be logged in"}
        try:
            success = self._login_manager.change_password(
                target_user, current_password, new_password, interface
            )
            if success:
                self._logger.add_event(
                    "CONFIGURATION",
                    f"Password changed for {target_user}",
                    user=current_user or target_user,
                )
                return {"success": True}
        except Exception as exc:  # pragma: no cover
            return {"success": False, "message": str(exc)}
        return {"success": False, "message": "Password change failed"}


class ControlPanelPasswordHandler:
    """Handles control panel password verification and updates."""

    def __init__(self, storage: StorageManager, lock_manager: LockManager):
        self._storage = storage
        self._lock = lock_manager

    def verify(self, password: str, require_master: bool, validate_fn) -> Dict:
        lock = self._lock.check_lock()
        if lock:
            return lock
        if not password:
            return self._lock.record_failure(message="Password required")
        username = "master" if require_master else "guest"
        if validate_fn(username, password, "control_panel"):
            self._lock.record_success()
            return {"success": True}
        return self._lock.record_failure(message="Incorrect password")

    def update_passwords(
        self, master_password: Optional[str], guest_password: Optional[str]
    ) -> Dict:
        updated = False
        if master_password:
            updated = self._update_cp_password("master", master_password) or updated
        if guest_password:
            updated = self._update_cp_password("guest", guest_password) or updated
        return {"success": updated}

    def _update_cp_password(self, username: str, new_password: str) -> bool:
        record = self._storage.get_login_interface(username, "control_panel")
        if not record:
            return False
        login_if = LoginInterface.from_dict(record)
        login_if.password_min_length = 4
        login_if.password_requires_digit = False
        login_if.password_requires_special = False
        login_if.set_password(new_password)
        login_if.login_attempts = 0
        login_if.is_locked = False
        self._storage.save_login_interface(login_if.to_dict())
        return True

