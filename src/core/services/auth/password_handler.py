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
            if not self._passwords_are_unique(new_password, target_user, interface):
                return {"success": False, "message": "Pin reserved"}
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

    def _passwords_are_unique(self, new_password: str, username: str, interface: str) -> bool:
        """Control-panel master/guest passwords must not match."""
        if interface != "control_panel" or username not in {"master", "guest"}:
            return True
        other_user = "guest" if username == "master" else "master"
        data = self._login_manager._storage_manager.get_login_interface(other_user, interface)
        if not data:
            return True
        other_login = LoginInterface.from_dict(data)
        return not other_login.verify_password(new_password)


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
        errors = False
        messages = []

        master_login = self._get_cp_login("master")
        guest_login = self._get_cp_login("guest")

        if master_password:
            if guest_login and guest_login.verify_password(master_password):
                messages.append("Master PIN unchanged: matches guest PIN.")
                errors = True
            elif self._update_cp_password("master", master_password):
                updated = True
                master_login = self._get_cp_login("master")
            else:
                messages.append("Master PIN not found.")
                errors = True

        if guest_password:
            # refresh master_login in case we just updated it above
            master_login = master_login or self._get_cp_login("master")
            if master_login and master_login.verify_password(guest_password):
                messages.append("Guest PIN unchanged: matches master PIN.")
                errors = True
            elif self._update_cp_password("guest", guest_password):
                updated = True
                guest_login = self._get_cp_login("guest")
            else:
                messages.append("Guest PIN not found.")
                errors = True

        success = updated and not errors
        result = {"success": success}
        if updated:
            result["updated"] = True
        if errors:
            result["errors"] = True
            if updated and not success:
                result["partial_success"] = True
        if messages:
            result["message"] = " ".join(messages)
        return result

    def _update_cp_password(self, username: str, new_password: str) -> bool:
        login_if = self._get_cp_login(username)
        if not login_if:
            return False
        login_if.password_min_length = 4
        login_if.password_requires_digit = False
        login_if.password_requires_special = False
        login_if.set_password(new_password)
        login_if.login_attempts = 0
        login_if.is_locked = False
        self._storage.save_login_interface(login_if.to_dict())
        return True

    def _get_cp_login(self, username: str) -> Optional[LoginInterface]:
        record = self._storage.get_login_interface(username, "control_panel")
        return LoginInterface.from_dict(record) if record else None

