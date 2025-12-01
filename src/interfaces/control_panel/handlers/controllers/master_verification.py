"""Master password verification helper."""

from __future__ import annotations

from typing import Callable, Dict

from .password_buffer import PasswordBuffer


class MasterVerification:
    """Allows verifying master password without logging in."""

    def __init__(self, send_request: Callable[..., Dict], display_cb: Callable[[str], None]):
        self._buffer = PasswordBuffer()
        self._send_request = send_request
        self._display_cb = display_cb

    def add_digit(self, digit: str, on_complete: Callable[[], None]):
        self._buffer.add_digit(digit, on_complete, self._display_cb)

    def verify(self) -> Dict:
        code = self._buffer.consume()
        if not code:
            return {"success": False, "message": "Enter password"}
        return self._send_request("verify_control_panel_password", password=code)

    def reset(self):
        self._buffer.reset()


