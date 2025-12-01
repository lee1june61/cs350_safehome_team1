"""Authentication and identity verification helpers."""

from __future__ import annotations

from typing import Dict, Optional

from ...configuration import LoginManager, StorageManager
from ..logging.system_logger import SystemLogger
from .auth.identity_controller import IdentityController
from .auth.login_coordinator import LoginCoordinator


class AuthService:
    """Thin façade that wires login + identity controllers."""

    def __init__(
        self,
        login_manager: LoginManager,
        logger: SystemLogger,
        storage_manager: StorageManager,
        *,
        max_attempts: int = 3,
        lock_duration: int = 60,
    ):
        self._identity = IdentityController(
            max_attempts=max_attempts, lock_duration=lock_duration
        )
        self._login = LoginCoordinator(
            login_manager=login_manager,
            storage_manager=storage_manager,
            logger=logger,
            identity=self._identity,
            max_attempts=max_attempts,
            lock_duration=lock_duration,
        )

    def login_control_panel(self, username="master", password="", **_) -> Dict:
        return self._login.login_control_panel(username=username, password=password)

    def login_web(
        self, user_id="", password="", password1="", password2="", **_
    ) -> Dict:
        return self._login.login_web(
            user_id=user_id, password=password, password1=password1, password2=password2
        )

    def legacy_web_login(
        self, user_id="", password="", password1="", password2="", **_
    ) -> Dict:
        return self._login.legacy_web_login(
            user_id=user_id, password=password, password1=password1, password2=password2
        )

    def logout(self, **_) -> Dict:
        return self._login.logout()

    def change_password(
        self,
        current_password="",
        new_password="",
        username="master",
        interface="control_panel",
        **_,
    ) -> Dict:
        return self._login.change_password(
            current_password=current_password,
            new_password=new_password,
            username=username,
            interface=interface,
        )

    def verify_control_panel_password(
        self, password: str = "", require_master: bool = True, **_
    ) -> Dict:
        return self._login.verify_control_panel_password(
            password=password, require_master=require_master
        )

    def update_control_panel_passwords(self, master_password=None, guest_password=None):
        return self._login.update_control_panel_passwords(
            master_password=master_password,
            guest_password=guest_password,
        )

    def update_policy(self, *, max_attempts=None, lock_duration=None):
        self._login.update_policy(
            max_attempts=max_attempts, lock_duration=lock_duration
        )

    def verify_identity(self, value="", **_) -> Dict:
        return self._identity.verify(value)

    def is_identity_verified(self, **_) -> Dict:
        return self._identity.is_verified()

    def set_identity_contact(self, phone: Optional[str]):
        self._identity.set_contact(phone)

    @property
    def current_user(self) -> Optional[str]:
        return self._login.current_user

    @property
    def access_level(self) -> Optional[int]:
        return self._login.access_level

    @property
    def is_verified(self) -> bool:
        """Backward-compatible boolean flag for legacy callers."""
        result = self._identity.is_verified()
        return bool(result.get("verified"))
