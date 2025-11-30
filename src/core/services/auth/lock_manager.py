"""Lock and attempt tracking for authentication workflows."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Dict, Optional


class LockManager:
    """Tracks login attempts and lock state."""

    def __init__(self, max_attempts: int, lock_duration: int):
        self._max_attempts = max_attempts
        self._lock_duration = lock_duration
        self._attempts = max_attempts
        self._locked = False
        self._lock_time: Optional[datetime] = None

    def check_lock(self) -> Optional[Dict[str, object]]:
        if not self._locked:
            return None
        if self._lock_time:
            elapsed = datetime.now() - self._lock_time
            if elapsed >= timedelta(seconds=self._lock_duration):
                self.unlock()
                return None
            seconds_remaining = max(
                0, self._lock_duration - int(elapsed.total_seconds())
            )
        else:
            seconds_remaining = self._lock_duration
        return {
            "success": False,
            "locked": True,
            "message": "System locked",
            "seconds_remaining": seconds_remaining,
        }

    def record_success(self):
        self._attempts = self._max_attempts
        self._locked = False
        self._lock_time = None

    def record_failure(self, message: Optional[str] = None) -> Dict[str, object]:
        self._attempts -= 1
        response: Dict[str, object] = {
            "success": False,
            "attempts_remaining": max(self._attempts, 0),
        }
        if message:
            response["message"] = message
        if self._attempts <= 0:
            self._locked = True
            self._lock_time = datetime.now()
            response["locked"] = True
            response["lock_duration"] = self._lock_duration
        return response

    def update_policy(
        self, *, max_attempts: Optional[int] = None, lock_duration: Optional[int] = None
    ):
        if max_attempts is not None and max_attempts > 0:
            self._max_attempts = max_attempts
            self._attempts = min(self._attempts, self._max_attempts)
        if lock_duration is not None and lock_duration > 0:
            self._lock_duration = lock_duration

    def unlock(self):
        self._locked = False
        self._attempts = self._max_attempts
        self._lock_time = None


