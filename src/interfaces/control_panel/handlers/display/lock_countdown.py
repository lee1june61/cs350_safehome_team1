"""Lock countdown helper."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:  # pragma: no cover
    from ..control_panel import SafeHomeControlPanel
    from .messages import DisplayMessages


class LockCountdown:
    """Schedules and updates LOCKED countdown text."""

    def __init__(self, panel: "SafeHomeControlPanel", messages: DisplayMessages):
        self._panel = panel
        self._messages = messages
        self._job: Optional[str] = None
        self._remaining = 0

    def start(self, total_seconds: int):
        self.cancel()
        self._remaining = max(1, int(total_seconds))
        self._tick()

    def cancel(self):
        if self._job:
            self._panel.after_cancel(self._job)
            self._job = None
        self._remaining = 0

    def _tick(self):
        if self._remaining <= 0:
            self._messages.show_locked("Wait 00 sec")
            self.cancel()
            return
        self._messages.show_locked(f"Wait {self._remaining:02d} sec")
        self._remaining -= 1
        self._job = self._panel.after(1000, self._tick)





