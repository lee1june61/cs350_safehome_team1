"""
Unit tests for LockManager covering lock timers, policy updates, and attempt flow.
"""

from datetime import datetime, timedelta

from src.core.services.auth.lock_manager import LockManager


class TestLockManager:
    def test_record_failure_locks_after_max_attempts(self, monkeypatch):
        manager = LockManager(max_attempts=2, lock_duration=5)

        first = manager.record_failure("bad credentials")
        assert first["success"] is False
        assert first["attempts_remaining"] == 1
        assert "locked" not in first

        # Force deterministic lock timestamp for assertions
        fake_now = datetime(2025, 1, 1, 0, 0, 0)
        monkeypatch.setattr("src.core.services.auth.lock_manager.datetime", MockDateTime(fake_now))

        second = manager.record_failure()
        assert second["locked"] is True
        assert second["lock_duration"] == 5
        assert manager.check_lock()["locked"] is True

    def test_check_lock_auto_unlocks_after_duration(self):
        manager = LockManager(max_attempts=1, lock_duration=1)
        manager._locked = True
        manager._lock_time = datetime.now() - timedelta(seconds=2)

        assert manager.check_lock() is None
        assert manager._locked is False
        assert manager._attempts == manager._max_attempts

    def test_check_lock_reports_remaining_time(self):
        manager = LockManager(max_attempts=1, lock_duration=10)
        manager._locked = True
        manager._lock_time = datetime.now() - timedelta(seconds=3)

        response = manager.check_lock()
        assert response["locked"] is True
        assert 6 <= response["seconds_remaining"] <= 10

    def test_record_success_and_update_policy_reset_state(self):
        manager = LockManager(max_attempts=3, lock_duration=60)
        manager.record_failure()
        manager.record_failure()
        manager.record_success()
        assert manager._attempts == 3
        assert manager._locked is False

        manager.update_policy(max_attempts=5, lock_duration=120)
        assert manager._max_attempts == 5
        assert manager._lock_duration == 120
        assert manager._attempts == 3  # attempts stay within new max until reduced

        manager.update_policy(max_attempts=2)
        assert manager._max_attempts == 2
        assert manager._attempts == 2


class MockDateTime:
    """Helper class to monkeypatch datetime.now() with a fixed value."""

    def __init__(self, fixed_now):
        self._fixed_now = fixed_now

    def now(self):
        return self._fixed_now


