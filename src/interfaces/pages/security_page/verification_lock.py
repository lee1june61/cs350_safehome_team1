"""Lock timer management for security verification."""

from __future__ import annotations

from typing import Optional, Callable
from tkinter import ttk


class VerificationLockTimer:
    """Displays countdown and handles unlock callbacks."""

    def __init__(self, frame, status_label: ttk.Label, entry: ttk.Entry, verify_button: ttk.Button):
        self._frame = frame
        self._status = status_label
        self._entry = entry
        self._button = verify_button
        self._job: Optional[str] = None
        self._seconds = 0
        self._message = ""

    def start(self, message: str, seconds: int, on_unlock: Callable[[], None]):
        self.cancel()
        self._message = message or "Verification locked"
        self._seconds = max(int(seconds or 0), 0)
        self._entry.config(state="disabled")
        self._button.config(state="disabled")
        self._tick(on_unlock)

    def _tick(self, on_unlock: Callable[[], None]):
        if self._seconds <= 0:
            self._status.config(text=self._message, foreground="red")
            self.cancel()
            on_unlock()
            return
        self._status.config(text=f"{self._message} ({self._seconds}s)", foreground="red")
        self._seconds -= 1
        self._job = self._frame.after(1000, lambda: self._tick(on_unlock))

    def cancel(self):
        if self._job:
            self._frame.after_cancel(self._job)
            self._job = None
        self._seconds = 0




