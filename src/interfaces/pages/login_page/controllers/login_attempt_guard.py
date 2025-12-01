"""Login attempt guard for the web login page."""

from __future__ import annotations

import time
from typing import Callable


class LoginAttemptGuard:
    """Tracks attempts and manages lockout countdown."""

    def __init__(self, max_attempts: int = 3, lock_seconds: int = 60):
        self._max_attempts = max_attempts
        self._lock_seconds = lock_seconds
        self._attempts = max_attempts
        self._locked = False
        self._started_at: float | None = None
        self._job: str | None = None

    def reset_attempts(self):
        self._attempts = self._max_attempts
        self._locked = False
        self._started_at = None

    def record_failure(self) -> bool:
        """Returns True if lockout should start."""
        self._attempts -= 1
        if self._attempts <= 0:
            self._locked = True
            self._started_at = time.time()
            return True
        return False

    def is_locked(self) -> bool:
        return self._locked

    def remaining_attempts(self) -> int:
        return self._attempts

    def start_countdown(self, schedule_fn: Callable[[int, Callable], str], tick_fn: Callable[[int], None], unlock_fn: Callable[[], None]):
        """Schedule recurring countdown updates."""
        self._cancel(schedule_fn)
        remaining = self._remaining_seconds()
        if remaining <= 0:
            unlock_fn()
            return
        tick_fn(remaining)
        self._job = schedule_fn(1000, lambda: self.start_countdown(schedule_fn, tick_fn, unlock_fn))

    def _remaining_seconds(self) -> int:
        if not self._started_at:
            return 0
        elapsed = time.time() - self._started_at
        return max(0, int(self._lock_seconds - elapsed))

    def _cancel(self, schedule_fn: Callable):
        if self._job:
            schedule_fn("cancel", self._job)  # sentinel to instruct page to cancel
            self._job = None

