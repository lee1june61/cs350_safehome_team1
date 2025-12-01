"""Buffer utilities for password entry."""

from __future__ import annotations

from typing import Callable


class PasswordBuffer:
    """Tracks digit entry and triggers callbacks when length reaches 4."""

    def __init__(self):
        self._value = ""

    def reset(self):
        self._value = ""

    def consume(self) -> str:
        value = self._value
        self._value = ""
        return value

    def add_digit(self, digit: str, on_complete: Callable[[], None], display_cb: Callable[[str], None]):
        self._value += digit
        display_cb("*" * len(self._value))
        if len(self._value) == 4:
            on_complete()

