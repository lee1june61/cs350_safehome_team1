"""Login attempt tracking and lockout policy."""

from __future__ import annotations


class LoginGuard:
    """Tracks remaining attempts and lockout duration."""

    def __init__(self, max_attempts: int, lock_time_ms: int):
        self._max_attempts = max_attempts
        self._attempts = max_attempts
        self._lock_time_ms = lock_time_ms

    @property
    def lock_time_ms(self) -> int:
        return self._lock_time_ms

    @property
    def lock_time_seconds(self) -> int:
        return max(1, self._lock_time_ms // 1000)

    def configure(self, *, max_attempts: int | None = None, lock_time_seconds: int | None = None):
        if max_attempts and max_attempts > 0:
            self._max_attempts = max_attempts
            self._attempts = max_attempts
        if lock_time_seconds and lock_time_seconds > 0:
            self._lock_time_ms = lock_time_seconds * 1000

    def record_failure(self):
        self._attempts -= 1

    def record_success(self):
        self._attempts = self._max_attempts

    def is_locked(self) -> bool:
        return self._attempts <= 0

    def remaining_attempts(self) -> int:
        return self._attempts





