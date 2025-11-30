"""Login workflow handlers."""

from __future__ import annotations

from typing import Dict

from ....configuration import AccessLevel
from .lock_manager import LockManager
from .user_resolver import ControlPanelUserResolver


class ControlPanelLoginHandler:
    """Handles control panel login logic."""

    def __init__(self, lock_manager: LockManager, resolver: ControlPanelUserResolver):
        self._lock = lock_manager
        self._resolver = resolver

    def attempt(self, username: str, password: str, login_fn, on_success) -> Dict:
        lock = self._lock.check_lock()
        if lock:
            return lock
        candidates = self._resolver.resolve(username, password)
        tried = set()
        for candidate in candidates:
            if candidate in tried:
                continue
            access_level = login_fn(candidate, password, "control_panel")
            if access_level is not None:
                on_success(candidate, access_level, "control_panel")
                level_name = (
                    "MASTER" if access_level == AccessLevel.MASTER_ACCESS else "GUEST"
                )
                return {"success": True, "access_level": level_name}
            tried.add(candidate)
        return self._lock.record_failure()


class WebLoginHandler:
    """Handles web login logic."""

    def __init__(self, lock_manager: LockManager):
        self._lock = lock_manager

    def attempt(
        self,
        user_id: str,
        password: str,
        password1: str,
        password2: str,
        login_fn,
        on_success,
    ) -> Dict:
        lock = self._lock.check_lock()
        if lock:
            return lock
        pwd = password or ""
        if password1 or password2:
            if not password1 or not password2:
                return self._lock.record_failure(message="Enter both passwords")
            if password1 != password2:
                return self._lock.record_failure(message="Passwords do not match")
            pwd = password1
        elif not pwd:
            return self._lock.record_failure(message="Password required")
        access_level = login_fn(user_id, pwd, "web")
        if access_level is not None:
            on_success(user_id, access_level, "web")
            return {"success": True}
        return self._lock.record_failure()

