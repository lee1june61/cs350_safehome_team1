"""Password handler for control panel."""
from typing import TYPE_CHECKING, Optional, Callable

from .controllers.password_buffer import PasswordBuffer
from .controllers.password_change_flow import PasswordChangeFlow
from .controllers.login_guard import LoginGuard
from .controllers.master_verification import MasterVerification

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class PasswordHandler:
    """Handles password input, login, and password change."""

    MAX_ATTEMPTS = 3
    LOCK_TIME_MS = 60000

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel
        self._buffer = PasswordBuffer()
        self._guard = LoginGuard(self.MAX_ATTEMPTS, self.LOCK_TIME_MS)
        self._change_flow = PasswordChangeFlow(panel.send_request, self._display_mask)
        self._master_verification = MasterVerification(panel.send_request, self._display_mask)
        self._access_level: Optional[str] = None

    # ------------------------------------------------------------------ #
    # Configuration
    # ------------------------------------------------------------------ #
    def configure_policy(self, *, max_attempts: Optional[int] = None, lock_time_seconds: Optional[int] = None):
        self._guard.configure(max_attempts=max_attempts, lock_time_seconds=lock_time_seconds)

    # ------------------------------------------------------------------ #
    # Password entry
    # ------------------------------------------------------------------ #
    def add_digit(self, digit: str, on_complete: Callable[[], None]):
        self._buffer.add_digit(digit, on_complete, self._display_mask)

    def clear_buffer(self):
        self._buffer.reset()

    def consume_buffer(self) -> str:
        return self._buffer.consume()

    # ------------------------------------------------------------------ #
    # Login / Attempts
    # ------------------------------------------------------------------ #
    def try_login(self) -> bool:
        code = self.consume_buffer()
        res = self._panel.send_request("login_control_panel", password=code)
        if res.get("success"):
            self._access_level = res.get("access_level", "GUEST")
            self._guard.record_success()
            return True
        self._guard.record_failure()
        return False

    def get_remaining_attempts(self) -> int:
        return self._guard.remaining_attempts()

    def is_locked_out(self) -> bool:
        return self._guard.is_locked()

    def unlock(self):
        self._guard.record_success()

    # ------------------------------------------------------------------ #
    # Password change
    # ------------------------------------------------------------------ #
    def start_change(self):
        self._change_flow.start()

    def add_new_digit(self, digit: str, on_complete: Callable[[], None]):
        self._change_flow.add_digit(digit, on_complete)

    def finish_change(self):
        self._change_flow.finish()

    # ------------------------------------------------------------------ #
    # Master verification (without login)
    # ------------------------------------------------------------------ #
    def verify_master_code(self):
        return self._master_verification.verify()

    def add_master_digit(self, digit: str, on_complete: Callable[[], None]):
        self._master_verification.add_digit(digit, on_complete)

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #
    def _display_mask(self, value: str):
        self._panel.set_display_short_message2(value)

    @property
    def access_level(self) -> Optional[str]:
        return self._access_level

    def is_master(self) -> bool:
        return self._access_level == "MASTER"

    @property
    def lock_time_ms(self) -> int:
        return self._guard.lock_time_ms

    @property
    def lock_time_seconds(self) -> int:
        return self._guard.lock_time_seconds

