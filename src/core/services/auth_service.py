"""Authentication and identity verification helpers."""

from __future__ import annotations

from typing import Dict, Optional

from ...configuration import AccessLevel, LoginManager, StorageManager
from ..logging.system_logger import SystemLogger
from .auth.lock_manager import LockManager
from .auth.identity_validator import IdentityValidator
from .auth.user_resolver import ControlPanelUserResolver


class AuthService:
    """Encapsulates login/logout, password changes, and identity verification."""

    def __init__(
        self,
        login_manager: LoginManager,
        logger: SystemLogger,
        storage_manager: StorageManager,
        *,
        max_attempts: int = 3,
        lock_duration: int = 60,
    ):
        self._login_manager = login_manager
        self._logger = logger
        self._storage = storage_manager
        self._lock_manager = LockManager(max_attempts, lock_duration)
        self._identity = IdentityValidator()
        self._resolver = ControlPanelUserResolver(storage_manager)
        self._current_user: Optional[str] = None
        self._access_level: Optional[int] = None
        if hasattr(self._login_manager, "configure_lockout"):
            self._login_manager.configure_lockout(
                max_attempts=max_attempts, enforce_lockout=False
            )

    # ------------------------------------------------------------------ #
    # Public properties
    # ------------------------------------------------------------------ #
    @property
    def current_user(self) -> Optional[str]:
        return self._current_user

    @property
    def access_level(self) -> Optional[int]:
        return self._access_level

    @property
    def is_verified(self) -> bool:
        return self._identity.verified

    # ------------------------------------------------------------------ #
    # Command handlers
    # ------------------------------------------------------------------ #
    def login_control_panel(self, username="master", password="", **_) -> Dict:
        lock = self._lock_manager.check_lock()
        if lock:
            return lock

        candidates = self._resolver.resolve(username, password)
        tried = set()
        for candidate in candidates:
            if candidate in tried:
                continue
            access_level = self._login(candidate, password, "control_panel")
            if access_level is not None:
                self._on_login_success(candidate, access_level, "control_panel")
                level_name = (
                    "MASTER" if access_level == AccessLevel.MASTER_ACCESS else "GUEST"
                )
                self._logger.add_event(
                    "LOGIN", f"Control panel login: {candidate}", user=candidate
                )
                return {"success": True, "access_level": level_name}
            tried.add(candidate)
        return self._lock_manager.record_failure()

    def login_web(
        self, user_id="", password="", password1="", password2="", **_
    ) -> Dict:
        lock = self._lock_manager.check_lock()
        if lock:
            return lock

        pwd = password or ""
        if password1 or password2:
            if not password1 or not password2:
                return self._lock_manager.record_failure(
                    message="Enter both passwords"
                )
            if password1 != password2:
                return self._lock_manager.record_failure(
                    message="Passwords do not match"
                )
            pwd = password1
        elif not pwd:
            return self._lock_manager.record_failure(message="Password required")

        access_level = self._login(user_id, pwd, "web")
        if access_level is not None:
            self._on_login_success(user_id, access_level, "web")
            self._logger.add_event("LOGIN", f"Web login: {user_id}", user=user_id)
            return {"success": True}

        return self._lock_manager.record_failure()

    def legacy_web_login(
        self, user_id="", password="", password1="", password2="", **_
    ) -> Dict:
        if not password1 and not password2 and password:
            password1 = password2 = password
        return self.login_web(
            user_id=user_id,
            password=password1,
            password1=password1,
            password2=password2,
        )

    def logout(self, **_) -> Dict:
        if self._current_user:
            self._logger.add_event(
                "LOGOUT",
                f"User logged out: {self._current_user}",
                user=self._current_user,
            )
        self._login_manager.logout()
        self._current_user = None
        self._access_level = None
        self._identity.reset()
        return {"success": True}

    def verify_identity(self, value="", **_) -> Dict:
        success, message = self._identity.verify(value)
        if success:
            return {"success": True}
        return {"success": False, "message": message}

    def is_identity_verified(self, **_) -> Dict:
        return {"success": True, "verified": self._identity.verified}

    def change_password(
        self,
        current_password="",
        new_password="",
        username="master",
        interface="control_panel",
        **_,
    ) -> Dict:
        target_user = username or "master"
        if not self._current_user:
            if not self._ensure_authenticated_for_change(
                target_user, current_password, interface
            ):
                return {"success": False, "message": "Must be logged in"}

        try:
            success = self._login_manager.change_password(
                target_user, current_password, new_password, interface
            )
            if success:
                self._logger.add_event(
                    "CONFIGURATION",
                    f"Password changed for {target_user}",
                    user=self._current_user or target_user,
                )
                return {"success": True}
        except Exception as exc:  # pragma: no cover
            return {"success": False, "message": str(exc)}

        return {"success": False, "message": "Password change failed"}

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _on_login_success(self, username: str, access_level: int, interface: str):
        self._current_user = username
        self._access_level = access_level
        self._identity.reset()
        self._lock_manager.record_success()

    def update_policy(
        self, *, max_attempts: Optional[int] = None, lock_duration: Optional[int] = None
    ):
        self._lock_manager.update_policy(
            max_attempts=max_attempts, lock_duration=lock_duration
        )
        if hasattr(self._login_manager, "configure_lockout"):
            self._login_manager.configure_lockout(
                max_attempts=max_attempts, enforce_lockout=False
            )

    def _ensure_authenticated_for_change(
        self, username: str, password: str, interface: str
    ) -> bool:
        if not password:
            return False
        access_level = self._login(username, password, interface)
        if access_level is None:
            return False
        self._on_login_success(username, access_level, interface)
        return True

    def _login(self, username: str, password: str, interface: str):
        try:
            return self._login_manager.login(username, password, interface)
        except Exception as exc:  # pragma: no cover - defensive logging
            self._logger.add_event(
                "LOGIN", f"{interface} login failed: {exc}", severity="WARNING"
            )
            return None
