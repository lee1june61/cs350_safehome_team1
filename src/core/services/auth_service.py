"""Authentication and identity verification helpers."""

from __future__ import annotations

from typing import Dict, Optional

from ...configuration import LoginManager, StorageManager
from ..logging.system_logger import SystemLogger
from .auth import (
    ControlPanelLoginHandler,
    ControlPanelPasswordHandler,
    IdentityValidator,
    LockManager,
    PasswordChangeHandler,
    WebLoginHandler,
    ControlPanelUserResolver,
    VerificationHandler,
)


class AuthService:
    """Encapsulates login/logout, password changes, and identity verification."""

    def __init__(
        self, login_manager: LoginManager, logger: SystemLogger,
        storage_manager: StorageManager, *, max_attempts: int = 3, lock_duration: int = 60,
    ):
        self._login_manager = login_manager
        self._logger = logger
        self._lock_manager = LockManager(max_attempts, lock_duration)
        self._cp_login = ControlPanelLoginHandler(
            self._lock_manager, ControlPanelUserResolver(storage_manager)
        )
        self._web_login = WebLoginHandler(self._lock_manager)
        self._pw_change = PasswordChangeHandler(login_manager, logger, self._lock_manager)
        self._cp_pw = ControlPanelPasswordHandler(storage_manager, self._lock_manager)
        self._verification = VerificationHandler(
            IdentityValidator(), LockManager(max_attempts, lock_duration)
        )
        self._current_user: Optional[str] = None
        self._access_level: Optional[int] = None

    @property
    def current_user(self) -> Optional[str]:
        return self._current_user

    @property
    def access_level(self) -> Optional[int]:
        return self._access_level

    @property
    def is_verified(self) -> bool:
        return self._verification.verified

    def login_control_panel(self, username="master", password="", **_) -> Dict:
        result = self._cp_login.attempt(username, password, self._login, self._on_login_success)
        if result.get("success"):
            self._logger.add_event("LOGIN", f"Control panel login: {username}", user=username)
        return result

    def login_web(self, user_id="", password="", password1="", password2="", **_) -> Dict:
        result = self._web_login.attempt(user_id, password, password1, password2, self._login, self._on_login_success)
        if result.get("success"):
            self._logger.add_event("LOGIN", f"Web login: {user_id}", user=user_id)
        return result

    def legacy_web_login(self, user_id="", password="", password1="", password2="", **_) -> Dict:
        if not password1 and not password2 and password:
            password1 = password2 = password
        return self.login_web(user_id=user_id, password1=password1, password2=password2)

    def logout(self, **_) -> Dict:
        if self._current_user:
            self._logger.add_event("LOGOUT", f"User logged out: {self._current_user}", user=self._current_user)
        self._login_manager.logout()
        self._current_user, self._access_level = None, None
        self._verification.reset()
        return {"success": True}

    def verify_identity(self, value="", **_) -> Dict:
        return self._verification.verify(value)

    def is_identity_verified(self, **_) -> Dict:
        return self._verification.is_verified()

    def change_password(self, current_password="", new_password="", username="master", interface="control_panel", **_) -> Dict:
        return self._pw_change.change(self._current_user, username, current_password, new_password, interface, self._ensure_auth)

    def verify_control_panel_password(self, password: str = "", require_master: bool = True, **_) -> Dict:
        return self._cp_pw.verify(password, require_master, self._login_manager.validate_credentials)

    def update_control_panel_passwords(self, master_password=None, guest_password=None):
        return self._cp_pw.update_passwords(master_password, guest_password)

    def update_policy(self, *, max_attempts=None, lock_duration=None):
        self._lock_manager.update_policy(max_attempts=max_attempts, lock_duration=lock_duration)

    def set_identity_contact(self, phone: Optional[str]):
        self._verification.set_contact(phone or "")

    def _on_login_success(self, username: str, access_level: int, interface: str):
        self._current_user, self._access_level = username, access_level
        self._verification.reset()
        self._lock_manager.record_success()

    def _ensure_auth(self, username: str, password: str, interface: str) -> bool:
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
        except Exception:
            return None
