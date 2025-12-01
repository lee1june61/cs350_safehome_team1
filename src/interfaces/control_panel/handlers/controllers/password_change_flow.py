"""Password change workflow helper."""

from __future__ import annotations

from typing import Callable

from .password_buffer import PasswordBuffer


class PasswordChangeFlow:
    """Manages collecting new password digits and submitting to system."""

    def __init__(self, send_request: Callable[..., dict], display_cb: Callable[[str], None]):
        self._buffer = PasswordBuffer()
        self._send_request = send_request
        self._display_cb = display_cb

    def start(self):
        self._buffer.reset()

    def reset(self):
        """Clear any in-progress password change input."""
        self._buffer.reset()

    def add_digit(self, digit: str, on_complete: Callable[[], None]):
        self._buffer.add_digit(digit, on_complete, self._display_cb)

    def finish(self, current_password: str):
        new_code = self._buffer.consume()
        if not new_code:
            return {"success": False, "message": "Enter password"}, ""
        response = self._send_request(
            "change_password",
            current_password=current_password,
            new_password=new_code,
        )
        return response, new_code


