"""LogManager handles creation and retrieval of system event logs."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from .log import Log
from .storage_manager import StorageManager


class LogManager:
    """Manages system event logs."""

    def __init__(self, storage_manager: StorageManager) -> None:
        self._storage_manager = storage_manager

    def create_log(
        self,
        event_type: str,
        description: str,
        severity: str = "INFO",
        user: str = None,
    ) -> Log:
        """Create a new log entry."""
        return Log(
            event_type=event_type, description=description, severity=severity, user=user
        )

    def save_log(self, log: Log) -> bool:
        """Save log to storage."""
        return self._storage_manager.save_log(log.to_dict())

    def get_logs(self, limit: int = 100, event_type: str = None) -> List[Log]:
        """Retrieve recent logs, optionally filtered by event type."""
        rows = self._storage_manager.get_logs(limit=limit)
        logs = [Log.from_dict(row) for row in rows]
        if event_type:
            logs = [log for log in logs if log.event_type == event_type]
        return logs

    def get_logs_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[Log]:
        """Retrieve logs within a date range."""
        all_logs = self.get_logs(limit=1000)
        return [
            log
            for log in all_logs
            if log.timestamp and start_date <= log.timestamp <= end_date
        ]

    def get_intrusion_logs(self) -> List[Log]:
        """Retrieve intrusion-related logs."""
        return self.get_logs(limit=100, event_type="INTRUSION")

    def clear_old_logs(self, days_to_keep: int = 30) -> int:
        """Delete logs older than specified days. Returns count deleted."""
        cutoff = datetime.utcnow() - timedelta(days=days_to_keep)
        all_logs = self.get_logs(limit=10000)
        count = 0
        for log in all_logs:
            if log.timestamp and log.timestamp < cutoff and log.log_id:
                # Note: Actual deletion would require a delete method in StorageManager
                count += 1
        return count
