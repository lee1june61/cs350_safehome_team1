"""Aggregates login/logout/change-password flows."""

from __future__ import annotations

from typing import Dict, Optional

from ...logging.system_logger import SystemLogger
from ....configuration import LoginManager, StorageManager
from .login_handler import ControlPanelLoginHandler, WebLoginHandler
from .password_handler import ControlPanelPasswordHandler, PasswordChangeHandler
from .user_resolver import ControlPanelUserResolver
from .lock_manager import LockManager
from .identity_controller import IdentityController
from .login_flows import ControlPanelLoginFlow, WebLoginFlow


class LoginCoordinator:
    """Handles all login/logout/password operations for AuthService."""

    def __init__(
        self,
        login_manager: LoginManager,
        storage_manager: StorageManager,
        logger: SystemLogger,
        identity: IdentityController,
        *,
        max_attempts: int,
        lock_duration: int,
    ):
        self._login_manager = login_manager
        self._logger = logger
        self._identity = identity
        self._cp_lock = LockManager(max_attempts, lock_duration)
        self._web_lock = LockManager(max_attempts, lock_duration)
        cp_handler = ControlPanelLoginHandler(self._cp_lock, ControlPanelUserResolver(storage_manager))
        self._cp_flow = ControlPanelLoginFlow(cp_handler, logger, self._on_login_success)
        self._web_flow = WebLoginFlow(WebLoginHandler(self._web_lock), logger, self._on_login_success)
        self._pw_change = PasswordChangeHandler(login_manager, logger, self._cp_lock)
        self._cp_pw = ControlPanelPasswordHandler(storage_manager, self._cp_lock)

        self._current_user: Optional[str] = None
        self._access_level: Optional[int] = None

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #
    def login_control_panel(self, username="master", password="", **_) -> Dict:
        return self._cp_flow.login(username, password, self._login)

    def login_web(self, user_id="", password="", password1="", password2="", **_) -> Dict:
        return self._web_flow.login(user_id, password, password1, password2, self._login)

    def legacy_web_login(self, user_id="", password="", password1="", password2="", **_) -> Dict:
        if not password1 and not password2 and password:
            password1 = password2 = password
        return self.login_web(user_id=user_id, password1=password1, password2=password2)

    def logout(self, **_) -> Dict:
        if self._current_user:
            self._logger.add_event("LOGOUT", f"User logged out: {self._current_user}", user=self._current_user)
        self._login_manager.logout()
        self._current_user, self._access_level = None, None
        self._identity.reset()
        self._cp_lock.record_success()
        self._web_lock.record_success()
        return {"success": True}

    def change_password(self, current_password="", new_password="", username="master", interface="control_panel", **_) -> Dict:
        return self._pw_change.change(
            self._current_user,
            username,
            current_password,
            new_password,
            interface,
            self._ensure_auth,
        )

    def verify_control_panel_password(self, password: str = "", require_master: bool = True, **_) -> Dict:
        return self._cp_pw.verify(password, require_master, self._login_manager.validate_credentials)

    def update_control_panel_passwords(self, master_password=None, guest_password=None):
        return self._cp_pw.update_passwords(master_password, guest_password)

    def update_policy(self, *, max_attempts=None, lock_duration=None):
        self._cp_lock.update_policy(max_attempts=max_attempts, lock_duration=lock_duration)
        self._web_lock.update_policy(max_attempts=max_attempts, lock_duration=lock_duration)

    # ------------------------------------------------------------------ #
    # State helpers
    # ------------------------------------------------------------------ #
    @property
    def current_user(self) -> Optional[str]:
        return self._current_user

    @property
    def access_level(self) -> Optional[int]:
        return self._access_level

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _on_login_success(self, username: str, access_level: int, interface: str):
        self._current_user, self._access_level = username, access_level
        self._identity.reset()
        if interface == "control_panel":
            self._cp_lock.record_success()
        elif interface == "web":
            self._web_lock.record_success()

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
        except Exception:  # pragma: no cover
            return None

