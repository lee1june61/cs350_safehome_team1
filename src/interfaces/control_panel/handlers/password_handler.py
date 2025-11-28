"""Password handler for control panel."""
from typing import TYPE_CHECKING, Callable, Optional

if TYPE_CHECKING:
    from ..control_panel import SafeHomeControlPanel


class PasswordHandler:
    """Handles password input, login, and password change."""

    MAX_ATTEMPTS = 3
    LOCK_TIME_MS = 60000

    def __init__(self, panel: "SafeHomeControlPanel"):
        self._panel = panel
        self._pw_buffer = ""
        self._new_pw_buffer = ""
        self._attempts = self.MAX_ATTEMPTS
        self._access_level: Optional[str] = None

    @property
    def access_level(self) -> Optional[str]:
        return self._access_level

    def reset(self):
        """Reset password state."""
        self._pw_buffer = ""
        self._access_level = None
        self._attempts = self.MAX_ATTEMPTS

    def add_digit(self, digit: str, on_complete: Callable[[], None]):
        """Add digit to password buffer."""
        self._pw_buffer += digit
        self._panel.set_display_short_message2("*" * len(self._pw_buffer))
        if len(self._pw_buffer) == 4:
            on_complete()

    def add_new_digit(self, digit: str, on_complete: Callable[[], None]):
        """Add digit to new password buffer."""
        self._new_pw_buffer += digit
        self._panel.set_display_short_message2("*" * len(self._new_pw_buffer))
        if len(self._new_pw_buffer) == 4:
            on_complete()

    def try_login(self) -> bool:
        """Attempt login. Returns True if successful."""
        res = self._panel.send_request("login_control_panel", password=self._pw_buffer)
        self._pw_buffer = ""

        if res.get("success"):
            self._access_level = res.get("access_level", "GUEST")
            self._attempts = self.MAX_ATTEMPTS
            return True

        self._attempts -= 1
        return False

    def get_remaining_attempts(self) -> int:
        return self._attempts

    def is_locked_out(self) -> bool:
        return self._attempts <= 0

    def unlock(self):
        """Reset attempts after lockout."""
        self._attempts = self.MAX_ATTEMPTS

    def is_master(self) -> bool:
        return self._access_level == "MASTER"

    def start_change(self):
        """Start password change process."""
        self._new_pw_buffer = ""

    def finish_change(self):
        """Complete password change."""
        self._panel.send_request("change_password", new_password=self._new_pw_buffer)
        self._new_pw_buffer = ""

